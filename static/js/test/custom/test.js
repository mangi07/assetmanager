"use strict";

import testTokens from "./testTokens.js"
import fw from "./testFramework.js"


function run() {
	var tests = [testTokens];
	var runner = new fw.TestRunner(tests);
	runner.runTests();
	runner.displayResults();
		
}

run();