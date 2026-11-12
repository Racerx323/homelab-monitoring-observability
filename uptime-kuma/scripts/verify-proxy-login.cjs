/* Private login acceptance. Credentials and tokens remain in memory only. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const crypto = require('node:crypto');
const https = require('node:https');
const { io } = require('/app/node_modules/socket.io-client');
const production = process.argv[2] === '--production';
assert.ok(production || process.argv[2] === '--staging');
const ca = production ? undefined : fs.readFileSync('/work/cert.pem');
let credentials;
try {
    credentials = production ? JSON.parse(fs.readFileSync(0, 'utf8')) : {
        username: 'local-qualification', password: crypto.randomBytes(32).toString('base64url'),
    };
    assert.ok(credentials && typeof credentials === 'object');
} catch {
    console.error('Invalid private credential input');
    process.exit(64);
}
const { username, password } = credentials;
assert.ok(typeof username === 'string' && username.length > 0 && username.length <= 256);
assert.ok(typeof password === 'string' && password.length > 0 && password.length <= 4096);
const port = production ? 443 : 8443;
const sockets = [];
const observations = [];
let stage = 'bootstrap';
let family = 'none';
function reportFailure(code) {
    // Only locally assigned enums leave this process: no messages, names or values.
    console.error(JSON.stringify({ stage, family, code }));
}
const deadline = setTimeout(() => {
    reportFailure('CLIENT_DEADLINE');
    process.exit(124);
}, 150000);

function failure(code) {
    return Object.assign(new Error('Private acceptance failed'), { code });
}
function connect(url, tls = true, setup = false) {
    return new Promise((resolve, reject) => {
        const socket = io(url, {
            autoConnect: false, transports: ['websocket'], reconnection: false, timeout: 10000,
            ...(tls ? { ca, rejectUnauthorized: true, servername: 'uptime.local.theama.co',
                extraHeaders: { Host: 'uptime.local.theama.co' } } : {}),
        });
        sockets.push(socket);
        let needsSetup = false;
        const timer = setTimeout(() => finish(failure('READINESS_TIMEOUT')), 10000);
        const setupRequired = () => { needsSetup = true; };
        const disconnected = () => finish(failure('SOCKET_DISCONNECTED'));
        const unexpected = () => finish(failure('UNEXPECTED_READINESS'));
        const ready = () => finish(needsSetup === setup ? null : failure('UNEXPECTED_READINESS'));
        function finish(error) {
            clearTimeout(timer);
            socket.off('setup', setupRequired);
            socket.off('loginRequired', ready);
            socket.off('autoLogin', unexpected);
            socket.off('disconnect', disconnected);
            socket.off('connect_error', finish);
            if (error) { socket.disconnect(); reject(error); } else resolve(socket);
        }
        socket.once('setup', setupRequired);
        // Transport connect precedes server handler registration. loginRequired
        // is emitted after registration, including when initial setup is needed.
        socket.once('loginRequired', ready);
        socket.once('autoLogin', unexpected);
        socket.once('disconnect', disconnected);
        socket.once('connect_error', finish);
        socket.connect();
    });
}
function ack(socket, event, ...args) {
    return new Promise((resolve, reject) => {
        if (!socket.connected) { reject(failure('SOCKET_DISCONNECTED')); return; }
        const disconnected = () => finish(failure('SOCKET_DISCONNECTED'));
        function finish(error, result) {
            socket.off('disconnect', disconnected);
            if (error) reject(error); else resolve(result);
        }
        socket.once('disconnect', disconnected);
        socket.timeout(10000).emit(event, ...args, (error, result) => {
            if (error) {
                const code = !socket.connected ? 'SOCKET_DISCONNECTED'
                    : (error.message === 'operation has timed out' ? 'ACK_TIMEOUT' : 'ACK_ERROR');
                finish(failure(code));
            } else finish(null, result);
        });
    });
}
function dashboard(host) {
    return new Promise((resolve, reject) => {
        const request = https.get({ hostname: host, port, path: '/dashboard',
            ca, rejectUnauthorized: true, servername: 'uptime.local.theama.co',
            headers: { Host: 'uptime.local.theama.co' }, agent: false, timeout: 10000 }, response => {
            response.resume();
            response.on('end', () => resolve(response.statusCode));
        });
        request.on('timeout', () => request.destroy(new Error('HTTP timeout')));
        request.on('error', reject);
    });
}
(async () => {
    if (!production) {
        stage = 'setup';
        const bootstrap = await connect('http://127.0.0.1:3001', false, true);
        // The fixture server is already ready before this client is launched.
        assert.equal((await ack(bootstrap, 'setup', username, password)).ok, true);
        bootstrap.disconnect();
    }
    for (const [addressFamily, host, url] of [
        ['ipv4', production ? '10.1.0.56' : '127.0.0.1', production ? 'https://10.1.0.56' : 'https://127.0.0.1:8443'],
        ['ipv6', production ? 'fd36:5aa8:6971:1::56' : '::1', production ? 'https://[fd36:5aa8:6971:1::56]' : 'https://[::1]:8443'],
    ]) {
        family = addressFamily;
        stage = 'dashboard';
        assert.equal(await dashboard(host), 200);
        stage = 'websocket-connect';
        const socket = await connect(url);
        stage = 'transport';
        assert.equal(socket.io.engine.transport.name, 'websocket');
        stage = 'unauthenticated-denial';
        assert.equal((await ack(socket, 'getMonitorList')).ok, false);
        stage = 'wrong-password-denial';
        const rejected = await ack(socket, 'login', { username, password: 'deliberately-wrong' });
        assert.equal(rejected.ok, false);
        stage = 'wrong-password-message';
        assert.equal(rejected.msg, 'authIncorrectCreds');
        stage = 'correct-login';
        assert.equal((await ack(socket, 'login', { username, password })).ok, true);
        stage = 'authenticated-list';
        assert.equal((await ack(socket, 'getMonitorList')).ok, true);
        stage = 'second-connect';
        const second = await connect(url);
        stage = 'second-login';
        assert.equal((await ack(second, 'login', { username, password })).ok, true);
        stage = 'second-list';
        assert.equal((await ack(second, 'getMonitorList')).ok, true);
        stage = 'logout';
        await ack(socket, 'logout');
        stage = 'logout-denial';
        assert.equal((await ack(socket, 'getMonitorList')).ok, false);
        socket.disconnect();
        observations.push({ family, host, second, rejected: 'authIncorrectCreds' });
    }
    // Exceeds two configured 30-second active-health intervals. This is not
    // direct evidence of each Caddy health request completing.
    stage = 'idle-wait';
    family = 'none';
    await new Promise(resolve => setTimeout(resolve, 65000));
    for (const row of observations) {
        family = row.family;
        stage = 'idle-dashboard';
        assert.equal(await dashboard(row.host), 200);
        stage = 'idle-list';
        assert.equal((await ack(row.second, 'getMonitorList')).ok, true);
        stage = 'idle-logout';
        await ack(row.second, 'logout');
        stage = 'idle-logout-denial';
        assert.equal((await ack(row.second, 'getMonitorList')).ok, false);
        console.log(JSON.stringify({ family: row.family, tls: production ? 'verified-system-trust' : 'verified-synthetic-CA',
            transport: 'websocket', dashboard: 200, rejection: row.rejected,
            immediateRetry: true, secondClient: true, idleSeconds: 65, logoutDenial: true }));
    }
})().catch(error => {
    const codes = new Set(['ECONNREFUSED', 'ECONNRESET', 'ETIMEDOUT', 'ENETUNREACH',
        'EHOSTUNREACH', 'CERT_HAS_EXPIRED', 'DEPTH_ZERO_SELF_SIGNED_CERT',
        'UNABLE_TO_VERIFY_LEAF_SIGNATURE', 'ERR_TLS_CERT_ALTNAME_INVALID', 'ERR_ASSERTION',
        'READINESS_TIMEOUT', 'SOCKET_DISCONNECTED', 'UNEXPECTED_READINESS', 'ACK_TIMEOUT', 'ACK_ERROR']);
    const code = codes.has(error.code) ? error.code : 'UNCLASSIFIED';
    reportFailure(code);
    process.exitCode = 1;
}).finally(() => {
    clearTimeout(deadline);
    sockets.forEach(socket => socket.disconnect());
});
