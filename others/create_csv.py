"""Script to create CSV file"""
import pandas as pd


def create():
    # import csv
    trip = pd.read_csv('../input_files/trips.csv')
    # multiply until number of row > x
    while trip.shape[0] < 50000000:
        trip = trip.append(trip)

    trip.reset_index(inplace=True)
    # save file.
    trip.to_csv('50mi.csv', index=False)


if __name__ == "__main__":
    create()
