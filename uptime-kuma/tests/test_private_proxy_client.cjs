/* Execute the actual client with in-memory transport doubles: no network or Podman. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { EventEmitter } = require('node:events');
const source = fs.readFileSync(path.join(__dirname, '../scripts/verify-proxy-login.cjs'), 'utf8');

async function run(fault) {
    const errors = [], rows = [];
    let count = 0, requests = 0;
    const fakeProcess = { argv: ['node', 'client', '--production'], exitCode: 0,
        exit(code) { this.exitCode = code; } };
    const io = () => {
        const index = ++count;
        const events = new EventEmitter();
        let loggedIn = false, ready = false;
        const socket = {
            connected: false,
            io: { engine: { transport: { name: 'websocket' } } },
            once: (event, callback) => events.once(event, callback),
            off: (event, callback) => events.off(event, callback),
            connect() {
                socket.connected = true;
                events.emit('connect');
                if (fault === 'readiness-timeout') return;
                if (fault === 'readiness-disconnect') { socket.disconnect(); return; }
                const announce = () => {
                    ready = true;
                    if (fault === 'unexpected-readiness') events.emit('autoLogin');
                    else events.emit('loginRequired');
                };
                if (fault === 'late-readiness') setImmediate(announce); else queueMicrotask(announce);
            },
            timeout() { return this; },
            emit(event, ...args) {
                assert.ok(ready, 'request before application readiness');
                const callback = args.pop();
                if (fault === 'ack-disconnect') { socket.disconnect(); return; }
                if (fault === 'ack-timeout' || fault === 'ack-error') {
                    callback(new Error(fault === 'ack-timeout' ? 'operation has timed out' : 'SENTINEL-TOKEN'));
                    return;
                }
                let result;
                if (event === 'login') {
                    loggedIn = args[0].password !== 'deliberately-wrong';
                    if (fault === 'correct-login' && index === 1) loggedIn = false;
                    if (fault === 'second-login' && index === 2) loggedIn = false;
                    result = { ok: loggedIn, msg: loggedIn ? '' : 'authIncorrectCreds', token: 'SENTINEL-TOKEN' };
                } else if (event === 'logout') {
                    loggedIn = false;
                    result = { ok: true };
                } else result = { ok: loggedIn };
                callback(null, result);
            },
            disconnect() { if (socket.connected) { socket.connected = false; events.emit('disconnect', 'SENTINEL-TOKEN'); } },
        };
        return socket;
    };
    const https = { get(options, callback) {
        requests++;
        const req = new EventEmitter();
        req.destroy = error => req.emit('error', error);
        if (fault === 'deadline') return req;
        queueMicrotask(() => {
            if (fault === 'tls' || fault === 'unknown' || (fault === 'ipv6' && requests === 2)) {
                const error = new Error('SENTINEL-PASSWORD SENTINEL-TOKEN');
                error.name = 'SENTINEL-USER';
                error.code = fault === 'unknown' ? 'SENTINEL-TOKEN' : 'UNABLE_TO_VERIFY_LEAF_SIGNATURE';
                req.emit('error', error);
            } else {
                const response = new EventEmitter();
                response.statusCode = fault === 'http' ? 503 : 200;
                response.resume = () => {};
                callback(response);
                response.emit('end');
            }
        });
        return req;
    } };
    vm.runInNewContext(source, {
        require(name) {
            if (name === 'node:fs') return { readFileSync: () => JSON.stringify({ username: 'SENTINEL-USER', password: 'SENTINEL-PASSWORD' }) };
            if (name === 'node:https') return https;
            if (name === '/app/node_modules/socket.io-client') return { io };
            return require(name);
        },
        process: fakeProcess,
        console: { error: line => errors.push(line), log: line => rows.push(JSON.parse(line)) },
        setTimeout(callback, ms) {
            if (ms === 65000) queueMicrotask(callback);
            if (ms === 150000 && fault === 'deadline') setImmediate(callback);
            if (ms === 10000 && fault === 'readiness-timeout') setImmediate(callback);
            return 1;
        },
        clearTimeout() {},
    });
    for (let i = 0; i < 8; i++) await new Promise(resolve => setImmediate(resolve));
    assert.ok(!JSON.stringify({ errors, rows }).includes('SENTINEL'));
    return { errors: errors.map(JSON.parse), rows, code: fakeProcess.exitCode };
}
(async () => {
    for (const [fault, stage, family, code] of [
        ['readiness-timeout', 'websocket-connect', 'ipv4', 'READINESS_TIMEOUT'],
        ['readiness-disconnect', 'websocket-connect', 'ipv4', 'SOCKET_DISCONNECTED'],
        ['unexpected-readiness', 'websocket-connect', 'ipv4', 'UNEXPECTED_READINESS'],
        ['ack-timeout', 'unauthenticated-denial', 'ipv4', 'ACK_TIMEOUT'],
        ['ack-error', 'unauthenticated-denial', 'ipv4', 'ACK_ERROR'],
        ['ack-disconnect', 'unauthenticated-denial', 'ipv4', 'SOCKET_DISCONNECTED'],
        ['tls', 'dashboard', 'ipv4', 'UNABLE_TO_VERIFY_LEAF_SIGNATURE'],
        ['unknown', 'dashboard', 'ipv4', 'UNCLASSIFIED'],
        ['http', 'dashboard', 'ipv4', 'ERR_ASSERTION'],
        ['correct-login', 'correct-login', 'ipv4', 'ERR_ASSERTION'],
        ['second-login', 'second-login', 'ipv4', 'ERR_ASSERTION'],
        ['ipv6', 'dashboard', 'ipv6', 'UNABLE_TO_VERIFY_LEAF_SIGNATURE'],
    ]) {
        const result = await run(fault);
        assert.equal(result.code, 1);
        assert.deepEqual(result.errors, [{ stage, family, code }]);
        assert.deepEqual(result.rows, []);
    }
    const deadline = await run('deadline');
    assert.equal(deadline.code, 124);
    assert.deepEqual(deadline.errors, [{ stage: 'dashboard', family: 'ipv4', code: 'CLIENT_DEADLINE' }]);
    const delayed = await run('late-readiness');
    assert.equal(delayed.code, 0);
    assert.equal(delayed.rows.length, 2);
    const passed = await run('none');
    assert.equal(passed.code, 0);
    assert.deepEqual(passed.errors, []);
    assert.deepEqual(passed.rows.map(row => row.family), ['ipv4', 'ipv6']);
    console.log('PASS: 13 client failure cases and immediate/delayed readiness success; no network');
})().catch(error => { console.error(error); process.exitCode = 1; });
