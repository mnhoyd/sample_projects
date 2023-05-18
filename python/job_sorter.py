
from datetime import datetime, date


class JobSearchSorter:
    def __init__(self):
        self.filename = input(f'Input filename: ')
        if self.filename[-4:] != '.txt':
            self.filename = self.filename + '.txt'
        infile = open(self.filename, 'r', encoding = 'utf-8')

        stilling = []
        firma = []
        dato = []
        URL = []

        for line in infile:
            still = line.split(' - ')
            firma.append(still[0])
            stilling.append(still[1])
            dato.append(still[2])
            URL.append(still[3])
        
        #infile.close()

        for i in range(len(dato)):
    
            temp = dato[i].split('.')
            temp2 = f'{temp[0]}-{temp[1]}-{temp[2]}'
            dato[i] = temp2

            temp_string = dato[i]

            dato[i] = datetime.strptime(temp_string, '%d-%m-%y').date()

        for i in range(len(dato)-1):
            for j in range(len(dato)-1):
                if dato[j+1] < dato[j]:
                    dato[j+1], dato[j] = dato[j], dato[j+1]
                    stilling[j+1], stilling[j] = stilling[j], stilling[j+1]
                    URL[j+1], URL[j] = URL[j], URL[j+1]
                    firma[j+1], firma[j] = firma[j], firma[j+1]
        
        self.dato = dato
        self.stilling = stilling
        self.URL = URL
        self.firma = firma

    def DeleteExpired(self):
        dato, stilling, URL, firma = self.dato, self.stilling, self.URL, self.firma

        today = date.today()

        n = len(dato)
        i = 0
        while n != 0 and i != len(dato):
            for j in range(n):
                try:
                    if dato[j] < today:
                        print(f' Stilling {stilling[j]} hos {firma[j]} har utløpt! \n')
                        a = input('Søkte du? (Y/N): ')
                        file = open('utlopt.txt', 'a', encoding = 'utf-8')
                        file.write(f'{dato[j]} - {firma[j]} - {stilling[j]} - {URL[j]} - {a} \n')

                        Rfile = open('Rutlopt.txt', 'a', encoding = 'utf-8')
                        Rfile.write(f'{dato[j]}, {firma[j]}, {a} \n')

                        file.close()
                        Rfile.close()

                        del dato[j]
                        del firma[j]
                        del stilling[j]
                        del URL[j]

                    elif dato[j] == today:
                        print(f'Stilling {stilling[j]} hos {firma[j]} utløper i dag!')
                except IndexError:
                    n = len(dato)
                    break
            i += 1
        print(f'Antall stillinger: {len(dato)}')

    def WriteSorted(self, filename = None):
        dato, stilling, URL, firma = self.dato, self.stilling, self.URL, self.firma

        if filename == None:
            outfile = open('jobs_sorted.txt', 'w', encoding = 'utf-8')
            if len(dato) != 0:
                for i in range(len(dato)):
                    outfile.write(f'{dato[i]} - {firma[i]} - {stilling[i]} - {URL[i]}')
                    outfile.write('\n')
            else:
                print(f'No jobs... All expired')
        
        else:
            if len(dato) != 0:
                if filename[-4] != '.txt':
                    filename = filename + '.txt'
                outfile = open(filename, 'w', encoding = 'utf-8')
                for i in range(len(dato)):
                    outfile.write(f'{dato[i]} - {firma[i]} - {stilling[i]} - {URL[i]}')
                    outfile.write('\n')
            else:
                print(f'No jobs... All expired')


if __name__ == '__main__':
    jss = JobSearchSorter()
    jss.DeleteExpired()
    jss.WriteSorted()



