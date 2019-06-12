import tokenUtils from "./../../tokens.js"
import fw from "./testFramework.js"

class TokensTestCase extends fw.TestCase {

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


export default {
	TokensTestCase,
}