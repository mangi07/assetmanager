"use strict";

import TokensTestCase from "./test/testTokens.js"
import fw from "./testFramework.js"


function run() {
	var tests = [TokensTestCase];
	var runner = new fw.TestRunner(tests);
	runner.runTestCases();
	runner.displayResults();
		
}

run();