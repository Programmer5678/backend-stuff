public static boolean acceptable(int score, int income, boolean authorized) {
    boolean highScore = score > 700;
    boolean medScore = score > 500 && score <= 700;

    boolean highIncome = income > 100000;
    boolean medIncome = income >= 40000 && income <= 100000;

    if (highScore) return true;
    if (highIncome) return true;

    if (medIncome && authorized && medScore) return true;

    return false;
}

public static boolean rejectable(int score, int income, boolean authorized) {
    return !acceptable(score, income, authorized);
}
