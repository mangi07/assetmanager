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

	constructor (testCases) {
		this.testCases = [].concat(testCases);
		this.results = [];
		this.total = testCases.length;
		this.failed = this.total;
	}

	runTests (testCase) {
		Object.values(testCase).map(test => {
			if (typeof test === 'function') {
				var result = test.call();
				this.results.push(result);
			}
		})
	}

	runTestCases () {
		for (var x = 0; x < this.testCases.length; x++) {
			var testCase = new this.testCases[x];
			var result = this.runTests(testCase);
			this.results.push(result);
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


export default {
	TestResult,
	TestRunner,
}