public int getIntProperty(Properties props, String property) {
    String valueString = props.getProperty(property);

    if (valueString == null) {
        throw new MissingPropertiesException(property);
    }

    int value = Integer.parseInt(valueString);
    if (value <= 0) {
        throw new MissingPropertiesException(property + " > 0");
    }

    return value;
}

public int getInterval(Properties props) {
    return getIntProperty(props, "interval");
}

public int getTimeProperty(Properties props, String property, int interval) {
    int result = getIntProperty(props, property);

    if ((result % interval) != 0) {
        throw new MissingPropertiesException(property + " % checkInterval");
    }
    return result;
}

public int getDeparture(Properties props, int interval) {
    return getTimeProperty(props, "departure", interval);
}

public void getTimes(Properties props) throws Exception {
    int interval = getInterval(props);
    int duration = getTimeProperty(props, "duration", interval);
    int departure = getDeparture(props, interval);
}
