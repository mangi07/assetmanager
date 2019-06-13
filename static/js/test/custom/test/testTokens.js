import tokenUtils from "./../../../tokens.js"

export default class {

	testSetTokens() {
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

}
