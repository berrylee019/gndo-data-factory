from agents.nrc_agent import main as run_nrc
from agents.ap1000_agent import main as run_ap1000
from agents.apr1400_agent import main as run_apr1400

def main():

    print("Starting GNDO")

    run_nrc()
    run_ap1000()
    run_apr1400()

    print("Finished")

if __name__ == "__main__":
    main()
