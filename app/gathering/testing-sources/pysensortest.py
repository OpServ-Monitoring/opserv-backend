import sys

import sensors


def print_stuff():
    for chip in sensors.get_detected_chips():
        print(chip)

        for feature in chip.get_features():
            print('  {0}'.format(chip.get_label(feature)))

            for subfeature in chip.get_all_subfeatures(feature):
                print('    {0}{1}'.format(subfeature,
                                       chip.get_value(subfeature.number)))

            print()

def main():
    print_stuff()


if __name__ == '__main__':
    try:
        main()
    finally:
        sensors.cleanup()