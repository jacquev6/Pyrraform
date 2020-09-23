provider "empty" {
    # An unexpected configuration attribute in an unused provider doesn't seem to
    # trigger any error or warning
    unexpected = 42
}
