public class Matcher {

    public Matcher() {
    }

    public boolean match(int[] expected,
                         int[] actual,
                         int clipLimit,
                         int delta) {

        int[] clipped = applyCeiling(actual, clipLimit);

        return sameLength(clipped, expected) && diffWithinDelta(clipped, expected, delta);
    }

    private boolean sameLength(int[] actual, int[] expected) {
        return actual.length == expected.length;
    }

    private boolean diffWithinDelta(int[] actual, int[] expected, int delta) {

        boolean result = true;

        for (int i = 0; i < actual.length; i++) {
            if (Math.abs(expected[i] - actual[i]) > delta) {
                result = false;
                break; // stop early
            }
        }

        return result;
    }

    private int[] applyCeiling(int[] aArr, int ceiling) {
        return Arrays.stream(aArr)
                     .map(v -> Math.min(v, ceiling))
                     .toArray();
    }



}
