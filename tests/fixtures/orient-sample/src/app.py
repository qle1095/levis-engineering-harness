"""Print a one-line greeting."""


def greet(name="orient-sample"):
    return "hello from %s" % name


def main():
    print(greet())


if __name__ == "__main__":
    main()
