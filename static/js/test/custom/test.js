"use strict";

import tokenUtils from "./../../tokens.js"

class TestResult {

    constructor (should, expected, actual) {
        this.should = should;
        this.expected = expected;
        this.actual = actual;
    }

    passed () {
    	return this.expected === this.actual;
    }

    toString () {
    	var status = this.passed() ? "passed" : "failed";
        return `${this.should}\nExpected: ${this.expected}\nActual: ${this.actual}\nStatus: ${this.passed()}`;
    }

    print () {
      console.log( this.toString() );
    }
}

class TestRunner {

	constructor (tests) {
		this.tests = [].concat(tests);
		this.results = [];
		this.total = tests.length;
		this.failed = this.total;
	}

	runTests () {
		for (var x = 0; x < this.tests.length; x++) {
			this.results.push(this.tests[x]());
		}
	}

	displayResults () {
		var lenPassed = this.results.filter(it => it.passed).length;
		console.log(`Total tests run: ${this.total}`);
		console.log(`Total passed: ${lenPassed}`);
		for (var x = 0; x < this.results.length; x++) {
			console.log("~~~TEST~~~");
			this.results[x].print();
		};
	}

}

function testSetTokens() {
	var should = "setTokens should raise error when no arguments are passed";
	var expected = "In setTokens, access undefined.";
	var actual = null;

	try {
		var actual = tokenUtils.setTokens();
	} catch (error) {
		var actual = error;
	}

	return new TestResult(should, expected, actual);
}

function run() {
	var tests = [testSetTokens];
	var runner = new TestRunner(tests);
	runner.runTests();
	runner.displayResults();
		
}

run();