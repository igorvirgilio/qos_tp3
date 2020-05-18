from nfstream import NFStreamer
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display, HTML
from tkinter import *
from tabulate import tabulate

class Traff_Analy():
    def __init__(self):
        self.data = []
        self.cat_name = []
        self.app_name = []
        self.app_prot = []
        self.data_short = []
        self.data_dict = {}
        self.df_dict = []
        self.df_dict_stat = []
        self.df_cat_stat = []
        self.serv_info = []


    def capture(self):
        captura = NFStreamer(source='./Pcap_Files/webex-matheus.pcapng').to_pandas()
        #captura = NFStreamer(source='/home/igor/UMinho/MCT/captura/04-29_hang-spo-you-what.pcapng').to_pandas()
        #captura = NFStreamer(source='/home/igor/UMinho/MCT/mct_tp3/test.pcap').to_pandas()
        self.data = pd.DataFrame(captura) # converte em dataframe
        #pd.set_option('display.max_rows',320)
        print("\nA dimensão do arquivo é: ")
        print(self.data.shape)

    #def clean_DataFrame():
    #    self.data.rename(columns={'bidirectional_ip_bytes':'bid_'})

    def filtering(self):
        self.cat_name = self.data['category_name'].unique()
        self.app_name = self.data['application_name'].unique()
        self.app_prot = self.data['app_protocol'].unique()
        
        

        self.data_short = self.data.loc[0:,['src_ip','dst_ip',
                'bidirectional_ip_bytes','bidirectional_packets',
                #'src2dst_ip_bytes','dst2src_ip_bytes','app_protocol',
                #'src_port','dst_port','protocol','client_info',
                'server_info',
                #'bidirectional_duration_ms',
                'app_protocol','application_name','category_name',
                ]]
        # filtra por aplicações contidas na lista app_name
        #data_webex = (self.data_short['app_protocol'].isin(self.app_prot[1]))
        # filtra por aplicações que contenha a string 'Webex'
        #data_webex = (self.data_short['application_name'].str.contains('Webex'))
        
        # cria vários um dicionario com todas as tabelas separadas pela list criada em cat_name
        self.df_dict = {elem : pd.DataFrame for elem in self.cat_name}
        for key in self.df_dict.keys():
            self.df_dict[key] = self.data_short[:][self.data_short.category_name == key]
        
        #print(self.df_dict)



    def statistic(self):
        self.total_bi_bytes = (self.data_short['bidirectional_ip_bytes'].sum())/1000
        total_bi_packets = self.data_short['bidirectional_packets'].sum()
        total_flows = len(self.data_short.index)
        print('Total de bytes da captura: '+str(self.total_bi_bytes))
        print('Total de pacotes da captura: '+str(total_bi_packets))
        print('Total de fluxos da captura: '+str(total_flows))

        data_grouped = self.data.groupby(self.data_short.category_name)
        
        # Cria novo dicionario com a estrutuda do novo DataFrame
        data_cat = {'categoria':[],'total_bytes':[],'(%) do total':[],'Applicações':[],'# of Apps':[],'Most used server':[],} 
        self.df_cat_stat = pd.DataFrame(data_cat) # converte em DF pandas
        

        columns = list(self.df_cat_stat)
        data_dict = []

        i=0
        for x in self.cat_name:
            group_x = data_grouped.get_group(str(self.cat_name[i]))
            group_x_name = group_x.iloc[0]['category_name']

                      
            all_bytes = (group_x['bidirectional_ip_bytes'].sum())/1000
            print(all_bytes)
            percent_of = round(((all_bytes/self.total_bi_bytes)*100 ),2)
            #print(percent_of)
            app_per_cat = group_x['application_name'].unique()
            num_app = len(app_per_cat)
            group_x = group_x.sort_values(by='bidirectional_raw_bytes', ascending=False)

            # Coletando informação dos principais servidores da categoria
            server_freq = group_x['server_info'].value_counts()[:1].index.tolist()
            #print (group_x['server_info'])

            #server_freq = list(filter(None, group_x['server_info'][:1])
            server_freq = list(filter(None,group_x['server_info']))
            #print('\n')
            
            #print(server_freq)

            newlist = []
            j = 0
            for x in server_freq:
                if server_freq[j]:
                    newlist.extend(x.split(","))
                    j+=1  
                else:
                    pass

            if len(newlist) == 0:
                newlist = ['-']  
            
            for word in newlist[:]:
                if word.startswith('*'):
                    newlist.remove(word)
            print(newlist[0])
            

            print('\n----')
            values = [group_x_name, all_bytes, percent_of, app_per_cat, num_app, newlist[0]]
            zipped = zip(columns,values)

            dici = dict(zipped)
            data_dict.append(dici)

            i += 1

        # Faz o append do dicitionário no DataFrame e ordena descendentemente a partir do total de Bytes
        self.df_cat_stat = self.df_cat_stat.append(data_dict, True).sort_values(by='total_bytes', ascending=False)
        
        print(group_x)

    
    def print_table(self):
        i = 0
        
        for x in self.app_prot:
            #print('\n')
            #print(x)
            filt = (self.data_short['app_protocol'] == x) # Cria filtro p/ imprimir somente linhas que contenham o 'app_prot' x
            data_filt = self.data_short.loc[filt] # criar novo DataFrame com somente dados do app_prot x
            #print(data_filt['application_name'].loc[0])
 

            sum = data_filt['bidirectional_ip_bytes'].sum()
            self.data_dict.update({ self.app_name[i]: sum})
            i += 1  
            #print('O total de bytes transmitidos é de: '+str(sum)) 

                #i = 0 
        
        '''
            Imprime a table de uma categoria específica ou imprime 
            a tabela de todas as categorias.
        '''
        # Imprime uma tabela para cada categoria
        i = 0
        for x in self.cat_name:
            #print(self.cat_name[i])
            #print(self.df_dict[self.cat_name[i]])
            i += 1     
        #for key, value in mydic.items() :
        #    print (key, value)

        # Imprime tabela de estatísticas
        print(self.df_cat_stat)
        print ("Dataframe 1:")
        display(self.df_cat_stat.set_index('categoria'))
        print ("Dataframe 2:")
        display(HTML(self.df_cat_stat.to_html()))
    
    def plot_graphs(self):

        labels = self.df_cat_stat['categoria'].to_list()
        sizes = self.df_cat_stat['total_bytes'].to_list()
        
        # Plot
        plt.pie(sizes, labels=labels, #xplode=0.1, #colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)
        
        #patches, texts = plt.pie(sizes, shadow=True, startangle=90)
        #plt.legend(patches, labels, loc="best")
        #plt.tight_layout()

        plt.axis('equal')
        plt.show(block=FALSE)

    def plot_graphs2(self):
        fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

        recipe = self.df_cat_stat['categoria'].to_list()

        data = self.df_cat_stat['total_bytes'].to_list()

        wedges, texts = ax.pie(data, wedgeprops=dict(width=0.5), startangle=-40)

        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        kw = dict(arrowprops=dict(arrowstyle="-"),
                bbox=bbox_props, zorder=0, va="center")

        for i, p in enumerate(wedges):
            ang = (p.theta2 - p.theta1)/2. + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = "angle,angleA=0,angleB={}".format(ang)
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            ax.annotate(recipe[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                        horizontalalignment=horizontalalignment, **kw)

        ax.set_title("Matplotlib bakery: A donut")

        plt.show(block=FALSE)   
    
    def plot_graphs_barh(self):
        labels = self.df_cat_stat['categoria'].to_list()
        sizes = self.df_cat_stat['%% do total'].to_list()

        df = pd.DataFrame({'Total Bytes': sizes}, index=labels)
        ax = df.plot.barh(y='Total Bytes')

        plt.show(block=FALSE) 
    
    def win_table(self):
        win = Tk()
        
        pdtabulate=lambda df:tabulate(self.df_cat_stat.set_index('categoria'),headers='keys',tablefmt='psql')

        print(pdtabulate(self.df_cat_stat))

        table1 = Label(win, text=pdtabulate(self.df_cat_stat),font=('Consolas', 10), justify=LEFT, anchor='nw').grid(sticky='ewns')    
        #table2 = Label(win, text=self.df_cat_stat['total_bytes']).grid(column=1, row=0)
        win.mainloop()
   
    #def main(self):
    #    #traff = Traff_Analy()
#
    #    self.capture()
    #    self.filtering()
    #    self.statistic()
    #    self.print_table()
    #    #self.plot_graphs_barh()
    #    self.plot_graphs()
    #    
    #    self.win_table()
    #    #self.plot_graphs2()

def main():
        traff = Traff_Analy()

        traff.capture()
        traff.filtering()
        traff.statistic()
        traff.print_table()
        #traff.plot_graphs_barh()
        traff.plot_graphs()
        
        traff.win_table()
        #traff.plot_graphs2()
    

if __name__ == '__main__':
    main() 

