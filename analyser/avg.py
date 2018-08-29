COUNT = 200 """How many elements should be averaged"""

def main(file):
    """Takes the result file and makes a new file wich contains the averaged values"""
    n_file = str(file) + "_avg_" + str(COUNT) + ".txt"
    file = str(file) + ".txt"

    n = 0
    s = 0
    for line in open(file):
        n += 1
        s += float(line)
        
        if n == COUNT:
            avg = s / n
            s = 0
            n = 0
            with open(n_file, 'a') as out:
                out.write(str(avg) + '\n')  

    if n > 0:
        avg = s / n
        with open(n_file, 'a') as out:
            out.write(str(avg) + '\n')  

main("dist_15k_dqn_eps_decay")