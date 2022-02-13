if __name__ == "__main__":
    if input("Do you want the working version? (Y/n) ").lower() == "n":
        import python_2048
        python_2048.run()
    else:
        import python_2048_working
        python_2048_working.run()