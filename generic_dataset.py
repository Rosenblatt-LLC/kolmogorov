#! /usr/bin/env python3

import os
import re

'''
Note that the sample dir is expected to have the different classes (e.g.
not_distorted, less_distorted, more_distorted)
'''

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Invalid command usage:')
        print('Proper usage (replace <> fields with values):')
        print('\tgeneric_dataset <sample directory> <output directory>')
        print('  Or')
        print('\tgeneric_dataset <sample directory> <output directory> <sample class>=<ratio of existing samples>')
        sys.exit(1)

    samples_dir = sys.argv[1]
    output = sys.argv[2]
    if len(sys.argv) == 3:
        classes = {
            'not_distorted': 0.15,
            'less_distorted': 0.75,
            'more_distorted': 0.10
        }
    else:
        classes = {}

        for sample_opt in sys.argv[3:]:
            sample = sample_opt.split('=')
            if len(sample) != 2:
                print(f'invalid option: {sample_opt}. Sample options must look like: <sample class>=<float ratio>, e.g. not_distorted=0.15')
            classes[sample[0]] = float(sample[1])

    for distort_class, ratio in classes.items():
        img_dir = f'{samples_dir}/{distort_class}/'

        TRAINING = lambda img_dir: img_dir + 'training'
        VALIDATION = lambda img_dir: img_dir + 'validation'

        for SUBDIR in [TRAINING, VALIDATION]:
            for sat in os.listdir(SUBDIR(img_dir)):
                sat_dir = SUBDIR(img_dir)+'/'+sat
                samples = [name for name in os.listdir(sat_dir)]

                for i in range(round(len(samples) * ratio)):
                    copy_name = '{}.{}.png'.format(samples[i][:-4],distort_class)
                    copy_target = '{}/{}/{}'.format(SUBDIR(output), sat, copy_name)
                    original = sat_dir + '/' + samples[i]

                    # Because the imgage filenames contained parantheses at the time, they need to be escaped
                    copy_target = re.sub('\(', '\\\(', copy_target)
                    copy_target = re.sub('\)', '\\\)', copy_target)
                    original = re.sub('\(', '\\\(', original)
                    original = re.sub('\)', '\\\)', original)

                    os.makedirs(os.path.dirname(copy_target), exist_ok=True)
                    os.system('cp {} {}'.format(original, copy_target))
