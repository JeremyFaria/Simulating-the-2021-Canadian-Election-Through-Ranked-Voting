import numpy as np
import pandas as pd
import random

def next_choice_sim(alpha):
    dirichlet_sample = np.random.dirichlet(alpha)
    index = np.random.choice(len(dirichlet_sample), p = dirichlet_sample)
    return index

def unstratified_borda(data, second_choice_matrix, number_of_simulations):
    #defining parameters
    conservative_scores = np.ones(number_of_simulations)
    ndp_scores = np.ones(number_of_simulations)
    liberal_scores = np.ones(number_of_simulations)
    ppc_scores = np.ones(number_of_simulations)
    green_scores = np.ones(number_of_simulations)
    bloc_scores = np.ones(number_of_simulations)

    for i in range(number_of_simulations):

        current_conservative_seats = 0
        current_ndp_seats = 0
        current_liberal_seats = 0
        current_ppc_seats = 0
        current_green_seats = 0
        current_bloc_seats = 0

        for k in range(338):

            current_conservative_score = 0
            current_ndp_score = 0
            current_liberal_score = 0
            current_ppc_score = 0
            current_green_score = 0
            current_bloc_score = 0

            for j in range(50):

                riding_number = np.random.randint(0,337)
                row = data.loc[riding_number]
                first_choice_proportion = np.ones(6)
                first_choice_proportion[0] = row[2]/row[9]
                first_choice_proportion[1] = row[3]/row[9]
                first_choice_proportion[2] = row[4]/row[9]
                first_choice_proportion[3] = row[5]/row[9]
                first_choice_proportion[4] = row[6]/row[9]
                first_choice_proportion[5] = row[7]/row[9]

                index_of_top_vote = next_choice_sim(first_choice_proportion)
                alpha = np.array(second_choice_matrix[index_of_top_vote])

                if index_of_top_vote == 0:
                    #order: conservative
                    current_conservative_score += 5
                    index_of_second_vote = next_choice_sim(alpha)
                    
                    if index_of_second_vote == 0:
                        #order: conservative, ndp
                        current_ndp_score += 4
                        alpha = np.delete(alpha, index_of_second_vote)
                        index_of_third_vote = next_choice_sim(alpha)

                        if index_of_third_vote == 0:
                            #order: conservative, ndp, liberal
                            current_liberal_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: conservative, ndp, liberal, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, ndp, liberal, ppc, green, bloc
                                    current_green_score += 1
                                
                                else:
                                    #order: conservative, ndp, liberal, ppc, bloc, green
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: conservative, ndp, liberal, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, ndp, liberal, green, ppc, bloc
                                    current_ppc_score += 1
                                
                                else:
                                    #order: conservative, ndp, liberal, green, bloc, ppc
                                    current_bloc_score += 1
                            
                            else:
                                #order: conservative, ndp, liberal, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, ndp, liberal, bloc, ppc, green
                                    current_ppc_score += 1
                                
                                else:
                                    #order: conservative, ndp, liberal, bloc, green, ppc
                                    current_green_score += 1
                        
                        elif index_of_third_vote == 1:
                            #order: conservative, ndp, ppc
                            current_ppc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: conservative, ndp, ppc, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, ndp, ppc, liberal, green, bloc
                                    current_green_score += 1
                                
                                else:
                                    #order: conservative, ndp, ppc, liberal, bloc, green
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: conservative, ndp, ppc, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, ndp, ppc, green, liberal, bloc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: conservative, ndp, ppc, green, bloc, liberal
                                    current_bloc_score += 1
                            
                            else:
                                #order: conservative, ndp, ppc, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, ndp, ppc, bloc, liberal, green
                                    current_liberal_score += 1
                                
                                else:
                                    #order: conservative, ndp, ppc, bloc, green, liberal
                                    current_green_score += 1

                        elif index_of_third_vote == 2:
                            #order: conservative, ndp, green
                            current_green_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: conservative, ndp, green, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, ndp, green, liberal, ppc, bloc
                                    current_ppc_score += 1
                                
                                else:
                                    #order: conservative, ndp, green, liberal, bloc, ppc
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: conservative, ndp, green, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, ndp, green, ppc, liberal, bloc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: conservative, ndp, green, ppc, bloc, liberal
                                    current_bloc_score += 1
                            
                            else:
                                #order: conservative, ndp, green, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, ndp, green, bloc, liberal, ppc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: conservative, ndp, green, bloc, ppc, liberal
                                    current_ppc_score += 1
                        
                        else:
                            #order: conservative, ndp, bloc
                            current_bloc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: conservative, ndp, bloc, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, ndp, bloc, liberal, ppc, green
                                    current_ppc_score += 1
                                
                                else:
                                    #order: conservative, ndp, bloc, liberal, green, ppc
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: conservative, ndp, bloc, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, ndp, bloc, ppc, liberal, green
                                    current_liberal_score += 1
                                
                                else:
                                    #order: conservative, ndp, bloc, ppc, green, liberal
                                    current_green_score += 1
                            
                            else:
                                #order: conservative, ndp, bloc, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, ndp, bloc, green, liberal, ppc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: conservative, ndp, bloc, green, ppc, liberal
                                    current_ppc_score += 1

                    elif index_of_second_vote == 1:
                        #order: conservative, liberal
                        current_liberal_score += 4
                        alpha = np.delete(alpha, index_of_second_vote)
                        index_of_third_vote = next_choice_sim(alpha)

                        if index_of_third_vote == 0:
                            #order: conservative, liberal, ndp
                            current_ndp_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: conservative, liberal, ndp, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, liberal, ndp, ppc, green, bloc
                                    current_green_score += 1
                                
                                else:
                                    #order: conservative, liberal, ndp, ppc, bloc, green
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: conservative, liberal, ndp, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, liberal, ndp, green, ppc, bloc
                                    current_ppc_score += 1
                                
                                else:
                                    #order: conservative, liberal, ndp, green, bloc, ppc
                                    current_bloc_score += 1
                            
                            else:
                                #order: conservative, liberal, ndp, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, liberal, ndp, bloc, ppc, green
                                    current_ppc_score += 1
                                
                                else:
                                    #order: conservative, liberal, ndp, bloc, green, ppc
                                    current_green_score += 1
                        
                        elif index_of_third_vote == 1:
                            #order: conservative, liberal, ppc
                            current_ppc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: conservative, liberal, ppc, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, liberal, ppc, ndp, green, bloc
                                    current_green_score += 1
                                
                                else:
                                    #order: conservative, liberal, ppc, ndp, bloc, green
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: conservative, liberal, ppc, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, liberal, ppc, green, ndp, bloc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: conservative, liberal, ppc, green, bloc, ndp
                                    current_bloc_score += 1
                            
                            else:
                                #order: conservative, liberal, ppc, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, liberal, ppc, bloc, ndp, green
                                    current_ndp_score += 1
                                
                                else:
                                    #order: conservative, liberal, ppc, bloc, green, ndp
                                    current_green_score += 1

                        elif index_of_third_vote == 2:
                            #order: conservative, liberal, green
                            current_green_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: conservative, liberal, green, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, liberal, green, ndp, ppc, bloc
                                    current_ppc_score += 1
                                
                                else:
                                    #order: conservative, liberal, green, ndp, bloc, ppc
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: conservative, liberal, green, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, liberal, green, ppc, ndp, bloc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: conservative, liberal, green, ppc, bloc, ndp
                                    current_bloc_score += 1
                            
                            else:
                                #order: conservative, liberal, green, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, liberal, green, bloc, ndp, ppc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: conservative, liberal, green, bloc, ppc, ndp
                                    current_ppc_score += 1
                        
                        else:
                            #order: conservative, liberal, bloc
                            current_bloc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: conservative, liberal, bloc, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, liberal, bloc, ndp, ppc, green
                                    current_ppc_score += 1
                                
                                else:
                                    #order: conservative, liberal, bloc, ndp, green, ppc
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: conservative, liberal, bloc, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, liberal, bloc, ppc, ndp, green
                                    current_ndp_score += 1
                                
                                else:
                                    #order: conservative, liberal, bloc, ppc, green, ndp
                                    current_green_score += 1
                            
                            else:
                                #order: conservative, liberal, bloc, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, liberal, bloc, green, ndp, ppc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: conservative, liberal, bloc, green, ppc, ndp
                                    current_ppc_score += 1
                    
                    elif index_of_second_vote == 2:
                        #order: conservative, ppc
                        current_ppc_score += 4
                        alpha = np.delete(alpha, index_of_second_vote)
                        index_of_third_vote = next_choice_sim(alpha)

                        if index_of_third_vote == 0:
                            #order: conservative, ppc, ndp
                            current_ndp_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: conservative, ppc, ndp, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, ppc, ndp, liberal, green, bloc
                                    current_green_score += 1
                                
                                else:
                                    #order: conservative, ppc, ndp, liberal, bloc, green
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: conservative, ppc, ndp, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, ppc, ndp, green, liberal, bloc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: conservative, ppc, ndp, green, bloc, liberal
                                    current_bloc_score += 1
                            
                            else:
                                #order: conservative, ppc, ndp, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, ppc, ndp, bloc, liberal, green
                                    current_liberal_score += 1
                                
                                else:
                                    #order: conservative, ppc, ndp, bloc, green, liberal
                                    current_green_score += 1
                        
                        elif index_of_third_vote == 1:
                            #order: conservative, ppc, liberal
                            current_liberal_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: conservative, ppc, liberal, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, ppc, liberal, ndp, green, bloc
                                    current_green_score += 1
                                
                                else:
                                    #order: conservative, ppc, liberal, ndp, bloc, green
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: conservative, ppc, liberal, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, ppc, liberal, green, ndp, bloc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: conservative, ppc, liberal, green, bloc, ndp
                                    current_bloc_score += 1
                            
                            else:
                                #order: conservative, ppc, liberal, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, ppc, liberal, bloc, ndp, green
                                    current_ndp_score += 1
                                
                                else:
                                    #order: conservative, ppc, liberal, bloc, green, ndp
                                    current_green_score += 1

                        elif index_of_third_vote == 2:
                            #order: conservative, ppc, green
                            current_green_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: conservative, ppc, green, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, ppc, green, ndp, liberal, bloc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: conservative, ppc, green, ndp, bloc, liberal
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: conservative, ppc, green, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, ppc, green, liberal, ndp, bloc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: conservative, ppc, green, liberal, bloc, ndp
                                    current_bloc_score += 1
                            
                            else:
                                #order: conservative, ppc, green, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, ppc, green, bloc, ndp, liberal
                                    current_ndp_score += 1
                                
                                else:
                                    #order: conservative, ppc, green, bloc, liberal, ndp
                                    current_liberal_score += 1
                        
                        else:
                            #order: conservative, ppc, bloc
                            current_bloc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: conservative, ppc, bloc, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, ppc, bloc, ndp, liberal, green
                                    current_liberal_score += 1
                                
                                else:
                                    #order: conservative, ppc, bloc, ndp, green, liberal
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: conservative, ppc, bloc, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, ppc, bloc, liberal, ndp, green
                                    current_ndp_score += 1
                                
                                else:
                                    #order: conservative, ppc, bloc, liberal, green, ndp
                                    current_green_score += 1
                            
                            else:
                                #order: conservative, ppc, bloc, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, ppc, bloc, green, ndp, liberal
                                    current_ndp_score += 1
                                
                                else:
                                    #order: conservative, ppc, bloc, green, liberal, ndp
                                    current_liberal_score += 1
                    
                    elif index_of_second_vote == 3:

                        #order: conservative, green
                        current_green_score += 4
                        alpha = np.delete(alpha, index_of_second_vote)
                        index_of_third_vote = next_choice_sim(alpha)

                        if index_of_third_vote == 0:
                            #order: conservative, green, ndp
                            current_ndp_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: conservative, green, ndp, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, green, ndp, liberal, ppc, bloc
                                    current_ppc_score += 1
                                
                                else:
                                    #order: conservative, green, ndp, liberal, bloc, ppc
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: conservative, green, ndp, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, green, ndp, ppc, liberal, bloc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: conservative, green, ndp, ppc, bloc, liberal
                                    current_bloc_score += 1
                            
                            else:
                                #order: conservative, green, ndp, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, green, ndp, bloc, liberal, ppc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: conservative, green, ndp, bloc, ppc, liberal
                                    current_ppc_score += 1
                        
                        elif index_of_third_vote == 1:
                            #order: conservative, green, liberal
                            current_liberal_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: conservative, green, liberal, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, green, liberal, ndp, ppc, bloc
                                    current_ppc_score += 1
                                
                                else:
                                    #order: conservative, green, liberal, ndp, bloc, ppc
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: conservative, green, liberal, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, green, liberal, ppc, ndp, bloc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: conservative, green, liberal, ppc, bloc, ndp
                                    current_bloc_score += 1
                            
                            else:
                                #order: conservative, green, liberal, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, green, liberal, bloc, ndp, ppc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: conservative, green, liberal, bloc, ppc, ndp
                                    current_ppc_score += 1

                        elif index_of_third_vote == 2:
                            #order: conservative, green, ppc
                            current_ppc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: conservative, green, ppc, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, green, ppc, ndp, liberal, bloc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: conservative, green, ppc, ndp, bloc, liberal
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: conservative, green, ppc, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, green, ppc, liberal, ndp, bloc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: conservative, green, ppc, liberal, bloc, ndp
                                    current_bloc_score += 1
                            
                            else:
                                #order: conservative, green, ppc, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, green, ppc, bloc, ndp, liberal
                                    current_ndp_score += 1
                                
                                else:
                                    #order: conservative, green, ppc, bloc, liberal, ndp
                                    current_liberal_score += 1
                        
                        else:
                            #order: conservative, green, bloc
                            current_bloc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: conservative, green, bloc, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, green, bloc, ndp, liberal, ppc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: conservative, green, bloc, ndp, ppc, liberal
                                    current_ppc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: conservative, green, bloc, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, green, bloc, liberal, ndp, ppc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: conservative, green, bloc, liberal, ppc, ndp
                                    current_ppc_score += 1
                            
                            else:
                                #order: conservative, green, bloc, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, green, bloc, ppc, ndp, liberal
                                    current_ndp_score += 1
                                
                                else:
                                    #order: conservative, green, bloc, ppc, liberal, ndp
                                    current_liberal_score += 1
                    
                    else:
                        #order: conservative, bloc
                        current_bloc_score += 4
                        alpha = np.delete(alpha, index_of_second_vote)
                        index_of_third_vote = next_choice_sim(alpha)

                        if index_of_third_vote == 0:
                            #order: conservative, bloc, ndp
                            current_ndp_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: conservative, bloc, ndp, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, bloc, ndp, liberal, ppc, green
                                    current_ppc_score += 1
                                
                                else:
                                    #order: conservative, bloc, ndp, liberal, green, ppc
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: conservative, bloc, ndp, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, bloc, ndp, ppc, liberal, green
                                    current_liberal_score += 1
                                
                                else:
                                    #order: conservative, bloc, ndp, ppc, green, liberal
                                    current_green_score += 1
                            
                            else:
                                #order: conservative, bloc, ndp, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, bloc, ndp, green, liberal, ppc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: conservative, bloc, ndp, green, ppc, liberal
                                    current_ppc_score += 1
                        
                        elif index_of_third_vote == 1:
                            #order: conservative, bloc, liberal
                            current_liberal_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: conservative, bloc, liberal, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, bloc, liberal, ndp, ppc, green
                                    current_ppc_score += 1
                                
                                else:
                                    #order: conservative, bloc, liberal, ndp, green, ppc
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: conservative, bloc, liberal, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, bloc, liberal, ppc, ndp, green
                                    current_ndp_score += 1
                                
                                else:
                                    #order: conservative, bloc, liberal, ppc, green, ndp
                                    current_green_score += 1
                            
                            else:
                                #order: conservative, bloc, liberal, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, bloc, liberal, green, ndp, ppc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: conservative, bloc, liberal, green, ppc, ndp
                                    current_ppc_score += 1

                        elif index_of_third_vote == 2:
                            #order: conservative, bloc, ppc
                            current_ppc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: conservative, bloc, ppc, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, bloc, ppc, ndp, liberal, green
                                    current_liberal_score += 1
                                
                                else:
                                    #order: conservative, bloc, ppc, ndp, green, liberal
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: conservative, bloc, ppc, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, bloc, ppc, liberal, ndp, green
                                    current_ndp_score += 1
                                
                                else:
                                    #order: conservative, bloc, ppc, liberal, green, ndp
                                    current_green_score += 1
                            
                            else:
                                #order: conservative, bloc, ppc, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, bloc, ppc, green, ndp, liberal
                                    current_ndp_score += 1
                                
                                else:
                                    #order: conservative, bloc, ppc, green, liberal, ndp
                                    current_liberal_score += 1
                        
                        else:
                            #order: conservative, bloc, green
                            current_green_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: conservative, bloc, green, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, bloc, green, ndp, liberal, ppc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: conservative, bloc, green, ndp, ppc, liberal
                                    current_ppc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: conservative, bloc, green, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, bloc, green, liberal, ndp, ppc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: conservative, bloc, green, liberal, ppc, ndp
                                    current_ppc_score += 1
                            
                            else:
                                #order: conservative, bloc, green, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: conservative, bloc, green, ppc, ndp, liberal
                                    current_ndp_score += 1
                                
                                else:
                                    #order: conservative, bloc, green, ppc, liberal, ndp
                                    current_liberal_score += 1

                elif index_of_top_vote == 1:
                    current_ndp_score += 5
                    #order: ndp
                    index_of_second_vote = next_choice_sim(alpha)
                    
                    if index_of_second_vote == 0:
                        #order: ndp, conservative
                        current_conservative_score += 4
                        alpha = np.delete(alpha, index_of_second_vote)
                        index_of_third_vote = next_choice_sim(alpha)

                        if index_of_third_vote == 0:
                            #order: ndp, conservative, liberal
                            current_liberal_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ndp, conservative, liberal, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, conservative, liberal, ppc, green, bloc
                                    current_green_score += 1
                                
                                else:
                                    #order: ndp, conservative, liberal, ppc, bloc, green
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ndp, conservative, liberal, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, conservative, liberal, green, ppc, bloc
                                    current_ppc_score += 1
                                
                                else:
                                    #order: ndp, conservative, liberal, green, bloc, ppc
                                    current_bloc_score += 1
                            
                            else:
                                #order: ndp, conservative, liberal, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, conservative, liberal, bloc, ppc, green
                                    current_ppc_score += 1
                                
                                else:
                                    #order: ndp, conservative, liberal, bloc, green, ppc
                                    current_green_score += 1
                        
                        elif index_of_third_vote == 1:
                            #order: ndp, conservative, ppc
                            current_ppc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ndp, conservative, ppc, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, conservative, ppc, liberal, green, bloc
                                    current_green_score += 1
                                
                                else:
                                    #order: ndp, conservative, ppc, liberal, bloc, green
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ndp, conservative, ppc, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, conservative, ppc, green, liberal, bloc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: ndp, conservative, ppc, green, bloc, liberal
                                    current_bloc_score += 1
                            
                            else:
                                #order: ndp, conservative, ppc, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, conservative, ppc, bloc, liberal, green
                                    current_liberal_score += 1
                                
                                else:
                                    #order: ndp, conservative, ppc, bloc, green, liberal
                                    current_green_score += 1

                        elif index_of_third_vote == 2:
                            #order: ndp, conservative, green
                            current_green_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ndp, conservative, green, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, conservative, green, liberal, ppc, bloc
                                    current_ppc_score += 1
                                
                                else:
                                    #order: ndp, conservative, green, liberal, bloc, ppc
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ndp, conservative, green, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, conservative, green, ppc, liberal, bloc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: ndp, conservative, green, ppc, bloc, liberal
                                    current_bloc_score += 1
                            
                            else:
                                #order: ndp, conservative, green, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, conservative, green, bloc, liberal, ppc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: ndp, conservative, green, bloc, ppc, liberal
                                    current_ppc_score += 1
                        
                        else:
                            #order: ndp, conservative, bloc
                            current_bloc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ndp, conservative, bloc, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, conservative, bloc, liberal, ppc, green
                                    current_ppc_score += 1
                                
                                else:
                                    #order: ndp, conservative, bloc, liberal, green, ppc
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ndp, conservative, bloc, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, conservative, bloc, ppc, liberal, green
                                    current_liberal_score += 1
                                
                                else:
                                    #order: ndp, conservative, bloc, ppc, green, liberal
                                    current_green_score += 1
                            
                            else:
                                #order: ndp, conservative, bloc, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, conservative, bloc, green, liberal, ppc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: ndp, conservative, bloc, green, ppc, liberal
                                    current_ppc_score += 1

                    elif index_of_second_vote == 1:
                        #order: ndp, liberal
                        current_liberal_score += 4
                        alpha = np.delete(alpha, index_of_second_vote)
                        index_of_third_vote = next_choice_sim(alpha)

                        if index_of_third_vote == 0:
                            #order: ndp, liberal, conservative
                            current_conservative_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ndp, liberal, conservative, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, liberal, conservative, ppc, green, bloc
                                    current_green_score += 1
                                
                                else:
                                    #order: ndp, liberal, conservative, ppc, bloc, green
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ndp, liberal, conservative, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, liberal, conservative, green, ppc, bloc
                                    current_ppc_score += 1
                                
                                else:
                                    #order: ndp, liberal, conservative, green, bloc, ppc
                                    current_bloc_score += 1
                            
                            else:
                                #order: ndp, liberal, conservative, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, liberal, conservative, bloc, ppc, green
                                    current_ppc_score += 1
                                
                                else:
                                    #order: ndp, liberal, conservative, bloc, green, ppc
                                    current_green_score += 1
                        
                        elif index_of_third_vote == 1:
                            #order: ndp, liberal, ppc
                            current_ppc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ndp, liberal, ppc, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, liberal, ppc, conservative, green, bloc
                                    current_green_score += 1
                                
                                else:
                                    #order: ndp, liberal, ppc, conservative, bloc, green
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ndp, liberal, ppc, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, liberal, ppc, green, conservative, bloc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ndp, liberal, ppc, green, bloc, conservative
                                    current_bloc_score += 1
                            
                            else:
                                #order: ndp, liberal, ppc, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, liberal, ppc, bloc, conservative, green
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ndp, liberal, ppc, bloc, green, conservative
                                    current_green_score += 1

                        elif index_of_third_vote == 2:
                            #order: ndp, liberal, green
                            current_green_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ndp, liberal, green, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, liberal, green, conservative, ppc, bloc
                                    current_ppc_score += 1
                                
                                else:
                                    #order: ndp, liberal, green, conservative, bloc, ppc
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ndp, liberal, green, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, liberal, green, ppc, conservative, bloc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ndp, liberal, green, ppc, bloc, conservative
                                    current_bloc_score += 1
                            
                            else:
                                #order: ndp, liberal, green, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, liberal, green, bloc, conservative, ppc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ndp, liberal, green, bloc, ppc, conservative
                                    current_ppc_score += 1
                        
                        else:
                            #order: ndp, liberal, bloc
                            current_bloc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ndp, liberal, bloc, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, liberal, bloc, conservative, ppc, green
                                    current_ppc_score += 1
                                
                                else:
                                    #order: ndp, liberal, bloc, conservative, green, ppc
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ndp, liberal, bloc, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, liberal, bloc, ppc, conservative, green
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ndp, liberal, bloc, ppc, green, conservative
                                    current_green_score += 1
                            
                            else:
                                #order: ndp, liberal, bloc, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, liberal, bloc, green, conservative, ppc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ndp, liberal, bloc, green, ppc, conservative
                                    current_ppc_score += 1
                    
                    elif index_of_second_vote == 2:
                        #order: ndp, ppc
                        current_ppc_score += 4
                        alpha = np.delete(alpha, index_of_second_vote)
                        index_of_third_vote = next_choice_sim(alpha)

                        if index_of_third_vote == 0:
                            #order: ndp, ppc, conservative
                            current_conservative_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ndp, ppc, conservative, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, ppc, conservative, liberal, green, bloc
                                    current_green_score += 1
                                
                                else:
                                    #order: ndp, ppc, conservative, liberal, bloc, green
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ndp, ppc, conservative, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, ppc, conservative, green, liberal, bloc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: ndp, ppc, conservative, green, bloc, liberal
                                    current_bloc_score += 1
                            
                            else:
                                #order: ndp, ppc, conservative, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, ppc, conservative, bloc, liberal, green
                                    current_liberal_score += 1
                                
                                else:
                                    #order: ndp, ppc, conservative, bloc, green, liberal
                                    current_green_score += 1
                        
                        elif index_of_third_vote == 1:
                            #order: ndp, ppc, liberal
                            current_liberal_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ndp, ppc, liberal, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, ppc, liberal, conservative, green, bloc
                                    current_green_score += 1
                                
                                else:
                                    #order: ndp, ppc, liberal, conservative, bloc, green
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ndp, ppc, liberal, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, ppc, liberal, green, conservative, bloc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ndp, ppc, liberal, green, bloc, conservative
                                    current_bloc_score += 1
                            
                            else:
                                #order: ndp, ppc, liberal, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, ppc, liberal, bloc, conservative, green
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ndp, ppc, liberal, bloc, green, conservative
                                    current_green_score += 1

                        elif index_of_third_vote == 2:
                            #order: ndp, ppc, green
                            current_green_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ndp, ppc, green, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, ppc, green, conservative, liberal, bloc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: ndp, ppc, green, conservative, bloc, liberal
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ndp, ppc, green, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, ppc, green, liberal, conservative, bloc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ndp, ppc, green, liberal, bloc, conservative
                                    current_bloc_score += 1
                            
                            else:
                                #order: ndp, ppc, green, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, ppc, green, bloc, conservative, liberal
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ndp, ppc, green, bloc, liberal, conservative
                                    current_liberal_score += 1
                        
                        else:
                            #order: ndp, ppc, bloc
                            current_bloc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ndp, ppc, bloc, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, ppc, bloc, conservative, liberal, green
                                    current_liberal_score += 1
                                
                                else:
                                    #order: ndp, ppc, bloc, conservative, green, liberal
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ndp, ppc, bloc, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, ppc, bloc, liberal, conservative, green
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ndp, ppc, bloc, liberal, green, conservative
                                    current_green_score += 1
                            
                            else:
                                #order: ndp, ppc, bloc, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, ppc, bloc, green, conservative, liberal
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ndp, ppc, bloc, green, liberal, conservative
                                    current_liberal_score += 1
                    
                    elif index_of_second_vote == 3:

                        #order: ndp, green
                        current_green_score += 4
                        alpha = np.delete(alpha, index_of_second_vote)
                        index_of_third_vote = next_choice_sim(alpha)

                        if index_of_third_vote == 0:
                            #order: ndp, green, conservative
                            current_conservative_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ndp, green, conservative, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, green, conservative, liberal, ppc, bloc
                                    current_ppc_score += 1
                                
                                else:
                                    #order: ndp, green, conservative, liberal, bloc, ppc
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ndp, green, conservative, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, green, conservative, ppc, liberal, bloc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: ndp, green, conservative, ppc, bloc, liberal
                                    current_bloc_score += 1
                            
                            else:
                                #order: ndp, green, conservative, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, green, conservative, bloc, liberal, ppc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: ndp, green, conservative, bloc, ppc, liberal
                                    current_ppc_score += 1
                        
                        elif index_of_third_vote == 1:
                            #order: ndp, green, liberal
                            current_liberal_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ndp, green, liberal, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, green, liberal, conservative, ppc, bloc
                                    current_ppc_score += 1
                                
                                else:
                                    #order: ndp, green, liberal, conservative, bloc, ppc
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ndp, green, liberal, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, green, liberal, ppc, conservative, bloc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ndp, green, liberal, ppc, bloc, conservative
                                    current_bloc_score += 1
                            
                            else:
                                #order: ndp, green, liberal, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, green, liberal, bloc, conservative, ppc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ndp, green, liberal, bloc, ppc, conservative
                                    current_ppc_score += 1

                        elif index_of_third_vote == 2:
                            #order: ndp, green, ppc
                            current_ppc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ndp, green, ppc, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, green, ppc, conservative, liberal, bloc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: ndp, green, ppc, conservative, bloc, liberal
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ndp, green, ppc, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, green, ppc, liberal, conservative, bloc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ndp, green, ppc, liberal, bloc, conservative
                                    current_bloc_score += 1
                            
                            else:
                                #order: ndp, green, ppc, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, green, ppc, bloc, conservative, liberal
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ndp, green, ppc, bloc, liberal, conservative
                                    current_liberal_score += 1
                        
                        else:
                            #order: ndp, green, bloc
                            current_bloc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ndp, green, bloc, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, green, bloc, conservative, liberal, ppc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: ndp, green, bloc, conservative, ppc, liberal
                                    current_ppc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ndp, green, bloc, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, green, bloc, liberal, conservative, ppc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ndp, green, bloc, liberal, ppc, conservative
                                    current_ppc_score += 1
                            
                            else:
                                #order: ndp, green, bloc, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, green, bloc, ppc, conservative, liberal
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ndp, green, bloc, ppc, liberal, conservative
                                    current_liberal_score += 1
                    
                    else:
                        #order: ndp, bloc
                        current_bloc_score += 4
                        alpha = np.delete(alpha, index_of_second_vote)
                        index_of_third_vote = next_choice_sim(alpha)

                        if index_of_third_vote == 0:
                            #order: ndp, bloc, conservative
                            current_conservative_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ndp, bloc, conservative, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, bloc, conservative, liberal, ppc, green
                                    current_ppc_score += 1
                                
                                else:
                                    #order: ndp, bloc, conservative, liberal, green, ppc
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ndp, bloc, conservative, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, bloc, conservative, ppc, liberal, green
                                    current_liberal_score += 1
                                
                                else:
                                    #order: ndp, bloc, conservative, ppc, green, liberal
                                    current_green_score += 1
                            
                            else:
                                #order: ndp, bloc, conservative, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, bloc, conservative, green, liberal, ppc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: ndp, bloc, conservative, green, ppc, liberal
                                    current_ppc_score += 1
                        
                        elif index_of_third_vote == 1:
                            #order: ndp, bloc, liberal
                            current_liberal_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ndp, bloc, liberal, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, bloc, liberal, conservative, ppc, green
                                    current_ppc_score += 1
                                
                                else:
                                    #order: ndp, bloc, liberal, conservative, green, ppc
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ndp, bloc, liberal, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, bloc, liberal, ppc, conservative, green
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ndp, bloc, liberal, ppc, green, conservative
                                    current_green_score += 1
                            
                            else:
                                #order: ndp, bloc, liberal, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, bloc, liberal, green, conservative, ppc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ndp, bloc, liberal, green, ppc, conservative
                                    current_ppc_score += 1

                        elif index_of_third_vote == 2:
                            #order: ndp, bloc, ppc
                            current_ppc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ndp, bloc, ppc, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, bloc, ppc, conservative, liberal, green
                                    current_liberal_score += 1
                                
                                else:
                                    #order: ndp, bloc, ppc, conservative, green, liberal
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ndp, bloc, ppc, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, bloc, ppc, liberal, conservative, green
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ndp, bloc, ppc, liberal, green, conservative
                                    current_green_score += 1
                            
                            else:
                                #order: ndp, bloc, ppc, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, bloc, ppc, green, conservative, liberal
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ndp, bloc, ppc, green, liberal, conservative
                                    current_liberal_score += 1
                        
                        else:
                            #order: ndp, bloc, green
                            current_green_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ndp, bloc, green, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, bloc, green, conservative, liberal, ppc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: ndp, bloc, green, conservative, ppc, liberal
                                    current_ppc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ndp, bloc, green, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, bloc, green, liberal, conservative, ppc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ndp, bloc, green, liberal, ppc, conservative
                                    current_ppc_score += 1
                            
                            else:
                                #order: ndp, bloc, green, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ndp, bloc, green, ppc, conservative, liberal
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ndp, bloc, green, ppc, liberal, conservative
                                    current_liberal_score += 1

                elif index_of_top_vote == 2:
                    #order: liberal
                    current_liberal_score += 5
                    index_of_second_vote = next_choice_sim(alpha)
                    
                    if index_of_second_vote == 0:
                        #order: liberal, conservative
                        current_conservative_score += 4
                        alpha = np.delete(alpha, index_of_second_vote)
                        index_of_third_vote = next_choice_sim(alpha)

                        if index_of_third_vote == 0:
                            #order: liberal, conservative, ndp
                            current_ndp_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: liberal, conservative, ndp, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, conservative, ndp, ppc, green, bloc
                                    current_green_score += 1
                                
                                else:
                                    #order: liberal, conservative, ndp, ppc, bloc, green
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: liberal, conservative, ndp, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, conservative, ndp, green, ppc, bloc
                                    current_ppc_score += 1
                                
                                else:
                                    #order: liberal, conservative, ndp, green, bloc, ppc
                                    current_bloc_score += 1
                            
                            else:
                                #order: liberal, conservative, ndp, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, conservative, ndp, bloc, ppc, green
                                    current_ppc_score += 1
                                
                                else:
                                    #order: liberal, conservative, ndp, bloc, green, ppc
                                    current_green_score += 1
                        
                        elif index_of_third_vote == 1:
                            #order: liberal, conservative, ppc
                            current_ppc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: liberal, conservative, ppc, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, conservative, ppc, ndp, green, bloc
                                    current_green_score += 1
                                
                                else:
                                    #order: liberal, conservative, ppc, ndp, bloc, green
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: liberal, conservative, ppc, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, conservative, ppc, green, ndp, bloc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: liberal, conservative, ppc, green, bloc, ndp
                                    current_bloc_score += 1
                            
                            else:
                                #order: liberal, conservative, ppc, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, conservative, ppc, bloc, ndp, green
                                    current_ndp_score += 1
                                
                                else:
                                    #order: liberal, conservative, ppc, bloc, green, ndp
                                    current_green_score += 1

                        elif index_of_third_vote == 2:
                            #order: liberal, conservative, green
                            current_green_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: liberal, conservative, green, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, conservative, green, ndp, ppc, bloc
                                    current_ppc_score += 1
                                
                                else:
                                    #order: liberal, conservative, green, ndp, bloc, ppc
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: liberal, conservative, green, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, conservative, green, ppc, ndp, bloc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: liberal, conservative, green, ppc, bloc, ndp
                                    current_bloc_score += 1
                            
                            else:
                                #order: liberal, conservative, green, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, conservative, green, bloc, ndp, ppc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: liberal, conservative, green, bloc, ppc, ndp
                                    current_ppc_score += 1
                        
                        else:
                            #order: liberal, conservative, bloc
                            current_bloc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: liberal, conservative, bloc, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, conservative, bloc, ndp, ppc, green
                                    current_ppc_score += 1
                                
                                else:
                                    #order: liberal, conservative, bloc, ndp, green, ppc
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: liberal, conservative, bloc, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, conservative, bloc, ppc, ndp, green
                                    current_ndp_score += 1
                                
                                else:
                                    #order: liberal, conservative, bloc, ppc, green, ndp
                                    current_green_score += 1
                            
                            else:
                                #order: liberal, conservative, bloc, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, conservative, bloc, green, ndp, ppc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: liberal, conservative, bloc, green, ppc, ndp
                                    current_ppc_score += 1

                    elif index_of_second_vote == 1:
                        #order: liberal, ndp
                        current_ndp_score += 4
                        alpha = np.delete(alpha, index_of_second_vote)
                        index_of_third_vote = next_choice_sim(alpha)

                        if index_of_third_vote == 0:
                            #order: liberal, ndp, conservative
                            current_conservative_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: liberal, ndp, conservative, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, ndp, conservative, ppc, green, bloc
                                    current_green_score += 1
                                
                                else:
                                    #order: liberal, ndp, conservative, ppc, bloc, green
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: liberal, ndp, conservative, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, ndp, conservative, green, ppc, bloc
                                    current_ppc_score += 1
                                
                                else:
                                    #order: liberal, ndp, conservative, green, bloc, ppc
                                    current_bloc_score += 1
                            
                            else:
                                #order: liberal, ndp, conservative, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, ndp, conservative, bloc, ppc, green
                                    current_ppc_score += 1
                                
                                else:
                                    #order: liberal, ndp, conservative, bloc, green, ppc
                                    current_green_score += 1
                        
                        elif index_of_third_vote == 1:
                            #order: liberal, ndp, ppc
                            current_ppc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: liberal, ndp, ppc, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, ndp, ppc, conservative, green, bloc
                                    current_green_score += 1
                                
                                else:
                                    #order: liberal, ndp, ppc, conservative, bloc, green
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: liberal, ndp, ppc, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, ndp, ppc, green, conservative, bloc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: liberal, ndp, ppc, green, bloc, conservative
                                    current_bloc_score += 1
                            
                            else:
                                #order: liberal, ndp, ppc, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, ndp, ppc, bloc, conservative, green
                                    current_conservative_score += 1
                                
                                else:
                                    #order: liberal, ndp, ppc, bloc, green, conservative
                                    current_green_score += 1

                        elif index_of_third_vote == 2:
                            #order: liberal, ndp, green
                            current_green_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: liberal, ndp, green, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, ndp, green, conservative, ppc, bloc
                                    current_ppc_score += 1
                                
                                else:
                                    #order: liberal, ndp, green, conservative, bloc, ppc
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: liberal, ndp, green, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, ndp, green, ppc, conservative, bloc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: liberal, ndp, green, ppc, bloc, conservative
                                    current_bloc_score += 1
                            
                            else:
                                #order: liberal, ndp, green, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, ndp, green, bloc, conservative, ppc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: liberal, ndp, green, bloc, ppc, conservative
                                    current_ppc_score += 1
                        
                        else:
                            #order: liberal, ndp, bloc
                            current_bloc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: liberal, ndp, bloc, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, ndp, bloc, conservative, ppc, green
                                    current_ppc_score += 1
                                
                                else:
                                    #order: liberal, ndp, bloc, conservative, green, ppc
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: liberal, ndp, bloc, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, ndp, bloc, ppc, conservative, green
                                    current_conservative_score += 1
                                
                                else:
                                    #order: liberal, ndp, bloc, ppc, green, conservative
                                    current_green_score += 1
                            
                            else:
                                #order: liberal, ndp, bloc, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, ndp, bloc, green, conservative, ppc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: liberal, ndp, bloc, green, ppc, conservative
                                    current_ppc_score += 1
                    
                    elif index_of_second_vote == 2:
                        #order: liberal, ppc
                        current_ppc_score += 4
                        alpha = np.delete(alpha, index_of_second_vote)
                        index_of_third_vote = next_choice_sim(alpha)

                        if index_of_third_vote == 0:
                            #order: liberal, ppc, conservative
                            current_conservative_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: liberal, ppc, conservative, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, ppc, conservative, ndp, green, bloc
                                    current_green_score += 1
                                
                                else:
                                    #order: liberal, ppc, conservative, ndp, bloc, green
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: liberal, ppc, conservative, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, ppc, conservative, green, ndp, bloc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: liberal, ppc, conservative, green, bloc, ndp
                                    current_bloc_score += 1
                            
                            else:
                                #order: liberal, ppc, conservative, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, ppc, conservative, bloc, ndp, green
                                    current_ndp_score += 1
                                
                                else:
                                    #order: liberal, ppc, conservative, bloc, green, ndp
                                    current_green_score += 1
                        
                        elif index_of_third_vote == 1:
                            #order: liberal, ppc, ndp
                            current_ndp_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: liberal, ppc, ndp, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, ppc, ndp, conservative, green, bloc
                                    current_green_score += 1
                                
                                else:
                                    #order: liberal, ppc, ndp, conservative, bloc, green
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: liberal, ppc, ndp, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, ppc, ndp, green, conservative, bloc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: liberal, ppc, ndp, green, bloc, conservative
                                    current_bloc_score += 1
                            
                            else:
                                #order: liberal, ppc, ndp, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, ppc, ndp, bloc, conservative, green
                                    current_conservative_score += 1
                                
                                else:
                                    #order: liberal, ppc, ndp, bloc, green, conservative
                                    current_green_score += 1

                        elif index_of_third_vote == 2:
                            #order: liberal, ppc, green
                            current_green_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: liberal, ppc, green, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, ppc, green, conservative, ndp, bloc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: liberal, ppc, green, conservative, bloc, ndp
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: liberal, ppc, green, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, ppc, green, ndp, conservative, bloc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: liberal, ppc, green, ndp, bloc, conservative
                                    current_bloc_score += 1
                            
                            else:
                                #order: liberal, ppc, green, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, ppc, green, bloc, conservative, ndp
                                    current_conservative_score += 1
                                
                                else:
                                    #order: liberal, ppc, green, bloc, ndp, conservative
                                    current_ndp_score += 1
                        
                        else:
                            #order: liberal, ppc, bloc
                            current_bloc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: liberal, ppc, bloc, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, ppc, bloc, conservative, ndp, green
                                    current_ndp_score += 1
                                
                                else:
                                    #order: liberal, ppc, bloc, conservative, green, ndp
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: liberal, ppc, bloc, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, ppc, bloc, ndp, conservative, green
                                    current_conservative_score += 1
                                
                                else:
                                    #order: liberal, ppc, bloc, ndp, green, conservative
                                    current_green_score += 1
                            
                            else:
                                #order: liberal, ppc, bloc, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, ppc, bloc, green, conservative, ndp
                                    current_conservative_score += 1
                                
                                else:
                                    #order: liberal, ppc, bloc, green, ndp, conservative
                                    current_ndp_score += 1
                    
                    elif index_of_second_vote == 3:

                        #order: liberal, green
                        current_green_score += 4
                        alpha = np.delete(alpha, index_of_second_vote)
                        index_of_third_vote = next_choice_sim(alpha)

                        if index_of_third_vote == 0:
                            #order: liberal, green, conservative
                            current_conservative_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: liberal, green, conservative, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, green, conservative, ndp, ppc, bloc
                                    current_ppc_score += 1
                                
                                else:
                                    #order: liberal, green, conservative, ndp, bloc, ppc
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: liberal, green, conservative, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, green, conservative, ppc, ndp, bloc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: liberal, green, conservative, ppc, bloc, ndp
                                    current_bloc_score += 1
                            
                            else:
                                #order: liberal, green, conservative, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, green, conservative, bloc, ndp, ppc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: liberal, green, conservative, bloc, ppc, ndp
                                    current_ppc_score += 1
                        
                        elif index_of_third_vote == 1:
                            #order: liberal, green, ndp
                            current_ndp_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: liberal, green, ndp, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, green, ndp, conservative, ppc, bloc
                                    current_ppc_score += 1
                                
                                else:
                                    #order: liberal, green, ndp, conservative, bloc, ppc
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: liberal, green, ndp, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, green, ndp, ppc, conservative, bloc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: liberal, green, ndp, ppc, bloc, conservative
                                    current_bloc_score += 1
                            
                            else:
                                #order: liberal, green, ndp, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, green, ndp, bloc, conservative, ppc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: liberal, green, ndp, bloc, ppc, conservative
                                    current_ppc_score += 1

                        elif index_of_third_vote == 2:
                            #order: liberal, green, ppc
                            current_ppc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: liberal, green, ppc, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, green, ppc, conservative, ndp, bloc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: liberal, green, ppc, conservative, bloc, ndp
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: liberal, green, ppc, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, green, ppc, ndp, conservative, bloc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: liberal, green, ppc, ndp, bloc, conservative
                                    current_bloc_score += 1
                            
                            else:
                                #order: liberal, green, ppc, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, green, ppc, bloc, conservative, ndp
                                    current_conservative_score += 1
                                
                                else:
                                    #order: liberal, green, ppc, bloc, ndp, conservative
                                    current_ndp_score += 1
                        
                        else:
                            #order: liberal, green, bloc
                            current_bloc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: liberal, green, bloc, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, green, bloc, conservative, ndp, ppc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: liberal, green, bloc, conservative, ppc, ndp
                                    current_ppc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: liberal, green, bloc, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, green, bloc, ndp, conservative, ppc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: liberal, green, bloc, ndp, ppc, conservative
                                    current_ppc_score += 1
                            
                            else:
                                #order: liberal, green, bloc, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, green, bloc, ppc, conservative, ndp
                                    current_conservative_score += 1
                                
                                else:
                                    #order: liberal, green, bloc, ppc, ndp, conservative
                                    current_ndp_score += 1
                    
                    else:
                        #order: liberal, bloc
                        current_bloc_score += 4
                        alpha = np.delete(alpha, index_of_second_vote)
                        index_of_third_vote = next_choice_sim(alpha)

                        if index_of_third_vote == 0:
                            #order: liberal, bloc, conservative
                            current_conservative_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: liberal, bloc, conservative, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, bloc, conservative, ndp, ppc, green
                                    current_ppc_score += 1
                                
                                else:
                                    #order: liberal, bloc, conservative, ndp, green, ppc
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: liberal, bloc, conservative, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, bloc, conservative, ppc, ndp, green
                                    current_ndp_score += 1
                                
                                else:
                                    #order: liberal, bloc, conservative, ppc, green, ndp
                                    current_green_score += 1
                            
                            else:
                                #order: liberal, bloc, conservative, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, bloc, conservative, green, ndp, ppc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: liberal, bloc, conservative, green, ppc, ndp
                                    current_ppc_score += 1
                        
                        elif index_of_third_vote == 1:
                            #order: liberal, bloc, ndp
                            current_ndp_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: liberal, bloc, ndp, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, bloc, ndp, conservative, ppc, green
                                    current_ppc_score += 1
                                
                                else:
                                    #order: liberal, bloc, ndp, conservative, green, ppc
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: liberal, bloc, ndp, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, bloc, ndp, ppc, conservative, green
                                    current_conservative_score += 1
                                
                                else:
                                    #order: liberal, bloc, ndp, ppc, green, conservative
                                    current_green_score += 1
                            
                            else:
                                #order: liberal, bloc, ndp, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, bloc, ndp, green, conservative, ppc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: liberal, bloc, ndp, green, ppc, conservative
                                    current_ppc_score += 1

                        elif index_of_third_vote == 2:
                            #order: liberal, bloc, ppc
                            current_ppc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: liberal, bloc, ppc, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, bloc, ppc, conservative, ndp, green
                                    current_ndp_score += 1
                                
                                else:
                                    #order: liberal, bloc, ppc, conservative, green, ndp
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: liberal, bloc, ppc, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, bloc, ppc, ndp, conservative, green
                                    current_conservative_score += 1
                                
                                else:
                                    #order: liberal, bloc, ppc, ndp, green, conservative
                                    current_green_score += 1
                            
                            else:
                                #order: liberal, bloc, ppc, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, bloc, ppc, green, conservative, ndp
                                    current_conservative_score += 1
                                
                                else:
                                    #order: liberal, bloc, ppc, green, ndp, conservative
                                    current_ndp_score += 1
                        
                        else:
                            #order: liberal, bloc, green
                            current_green_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: liberal, bloc, green, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, bloc, green, conservative, ndp, ppc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: liberal, bloc, green, conservative, ppc, ndp
                                    current_ppc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: liberal, bloc, green, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, bloc, green, ndp, conservative, ppc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: liberal, bloc, green, ndp, ppc, conservative
                                    current_ppc_score += 1
                            
                            else:
                                #order: liberal, bloc, green, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: liberal, bloc, green, ppc, conservative, ndp
                                    current_conservative_score += 1
                                
                                else:
                                    #order: liberal, bloc, green, ppc, ndp, conservative
                                    current_ndp_score += 1

                elif index_of_top_vote == 3:
                    #order: ppc
                    current_ppc_score += 5
                    index_of_second_vote = next_choice_sim(alpha)
                    
                    if index_of_second_vote == 0:
                        #order: ppc, conservative
                        current_conservative_score += 4
                        alpha = np.delete(alpha, index_of_second_vote)
                        index_of_third_vote = next_choice_sim(alpha)

                        if index_of_third_vote == 0:
                            #order: ppc, conservative, ndp
                            current_ndp_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ppc, conservative, ndp, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, conservative, ndp, liberal, green, bloc
                                    current_green_score += 1
                                
                                else:
                                    #order: ppc, conservative, ndp, liberal, bloc, green
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ppc, conservative, ndp, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, conservative, ndp, green, liberal, bloc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: ppc, conservative, ndp, green, bloc, liberal
                                    current_bloc_score += 1
                            
                            else:
                                #order: ppc, conservative, ndp, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, conservative, ndp, bloc, liberal, green
                                    current_liberal_score += 1
                                
                                else:
                                    #order: ppc, conservative, ndp, bloc, green, liberal
                                    current_green_score += 1
                        
                        elif index_of_third_vote == 1:
                            #order: ppc, conservative, liberal
                            current_liberal_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ppc, conservative, liberal, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, conservative, liberal, ndp, green, bloc
                                    current_green_score += 1
                                
                                else:
                                    #order: ppc, conservative, liberal, ndp, bloc, green
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ppc, conservative, liberal, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, conservative, liberal, green, ndp, bloc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: ppc, conservative, liberal, green, bloc, ndp
                                    current_bloc_score += 1
                            
                            else:
                                #order: ppc, conservative, liberal, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, conservative, liberal, bloc, ndp, green
                                    current_ndp_score += 1
                                
                                else:
                                    #order: ppc, conservative, liberal, bloc, green, ndp
                                    current_green_score += 1

                        elif index_of_third_vote == 2:
                            #order: ppc, conservative, green
                            current_green_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ppc, conservative, green, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, conservative, green, ndp, liberal, bloc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: ppc, conservative, green, ndp, bloc, liberal
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ppc, conservative, green, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, conservative, green, liberal, ndp, bloc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: ppc, conservative, green, liberal, bloc, ndp
                                    current_bloc_score += 1
                            
                            else:
                                #order: ppc, conservative, green, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, conservative, green, bloc, ndp, liberal
                                    current_ndp_score += 1
                                
                                else:
                                    #order: ppc, conservative, green, bloc, liberal, ndp
                                    current_liberal_score += 1
                        
                        else:
                            #order: ppc, conservative, bloc
                            current_bloc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ppc, conservative, bloc, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, conservative, bloc, ndp, liberal, green
                                    current_liberal_score += 1
                                
                                else:
                                    #order: ppc, conservative, bloc, ndp, green, liberal
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ppc, conservative, bloc, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, conservative, bloc, liberal, ndp, green
                                    current_ndp_score += 1
                                
                                else:
                                    #order: ppc, conservative, bloc, liberal, green, ndp
                                    current_green_score += 1
                            
                            else:
                                #order: ppc, conservative, bloc, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, conservative, bloc, green, ndp, liberal
                                    current_ndp_score += 1
                                
                                else:
                                    #order: ppc, conservative, bloc, green, liberal, ndp
                                    current_liberal_score += 1

                    elif index_of_second_vote == 1:
                        #order: ppc, ndp
                        current_ndp_score += 4
                        alpha = np.delete(alpha, index_of_second_vote)
                        index_of_third_vote = next_choice_sim(alpha)

                        if index_of_third_vote == 0:
                            #order: ppc, ndp, conservative
                            current_conservative_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ppc, ndp, conservative, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, ndp, conservative, liberal, green, bloc
                                    current_green_score += 1
                                
                                else:
                                    #order: ppc, ndp, conservative, liberal, bloc, green
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ppc, ndp, conservative, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, ndp, conservative, green, liberal, bloc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: ppc, ndp, conservative, green, bloc, liberal
                                    current_bloc_score += 1
                            
                            else:
                                #order: ppc, ndp, conservative, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, ndp, conservative, bloc, liberal, green
                                    current_liberal_score += 1
                                
                                else:
                                    #order: ppc, ndp, conservative, bloc, green, liberal
                                    current_green_score += 1
                        
                        elif index_of_third_vote == 1:
                            #order: ppc, ndp, liberal
                            current_liberal_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ppc, ndp, liberal, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, ndp, liberal, conservative, green, bloc
                                    current_green_score += 1
                                
                                else:
                                    #order: ppc, ndp, liberal, conservative, bloc, green
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ppc, ndp, liberal, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, ndp, liberal, green, conservative, bloc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ppc, ndp, liberal, green, bloc, conservative
                                    current_bloc_score += 1
                            
                            else:
                                #order: ppc, ndp, liberal, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, ndp, liberal, bloc, conservative, green
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ppc, ndp, liberal, bloc, green, conservative
                                    current_green_score += 1

                        elif index_of_third_vote == 2:
                            #order: ppc, ndp, green
                            current_green_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ppc, ndp, green, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, ndp, green, conservative, liberal, bloc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: ppc, ndp, green, conservative, bloc, liberal
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ppc, ndp, green, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, ndp, green, liberal, conservative, bloc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ppc, ndp, green, liberal, bloc, conservative
                                    current_bloc_score += 1
                            
                            else:
                                #order: ppc, ndp, green, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, ndp, green, bloc, conservative, liberal
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ppc, ndp, green, bloc, liberal, conservative
                                    current_liberal_score += 1
                        
                        else:
                            #order: ppc, ndp, bloc
                            current_bloc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ppc, ndp, bloc, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, ndp, bloc, conservative, liberal, green
                                    current_liberal_score += 1
                                
                                else:
                                    #order: ppc, ndp, bloc, conservative, green, liberal
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ppc, ndp, bloc, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, ndp, bloc, liberal, conservative, green
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ppc, ndp, bloc, liberal, green, conservative
                                    current_green_score += 1
                            
                            else:
                                #order: ppc, ndp, bloc, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, ndp, bloc, green, conservative, liberal
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ppc, ndp, bloc, green, liberal, conservative
                                    current_liberal_score += 1
                    
                    elif index_of_second_vote == 2:
                        #order: ppc, liberal
                        current_liberal_score += 4
                        alpha = np.delete(alpha, index_of_second_vote)
                        index_of_third_vote = next_choice_sim(alpha)

                        if index_of_third_vote == 0:
                            #order: ppc, liberal, conservative
                            current_conservative_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ppc, liberal, conservative, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, liberal, conservative, ndp, green, bloc
                                    current_green_score += 1
                                
                                else:
                                    #order: ppc, liberal, conservative, ndp, bloc, green
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ppc, liberal, conservative, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, liberal, conservative, green, ndp, bloc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: ppc, liberal, conservative, green, bloc, ndp
                                    current_bloc_score += 1
                            
                            else:
                                #order: ppc, liberal, conservative, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, liberal, conservative, bloc, ndp, green
                                    current_ndp_score += 1
                                
                                else:
                                    #order: ppc, liberal, conservative, bloc, green, ndp
                                    current_green_score += 1
                        
                        elif index_of_third_vote == 1:
                            #order: ppc, liberal, ndp
                            current_ndp_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ppc, liberal, ndp, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, liberal, ndp, conservative, green, bloc
                                    current_green_score += 1
                                
                                else:
                                    #order: ppc, liberal, ndp, conservative, bloc, green
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ppc, liberal, ndp, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, liberal, ndp, green, conservative, bloc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ppc, liberal, ndp, green, bloc, conservative
                                    current_bloc_score += 1
                            
                            else:
                                #order: ppc, liberal, ndp, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, liberal, ndp, bloc, conservative, green
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ppc, liberal, ndp, bloc, green, conservative
                                    current_green_score += 1

                        elif index_of_third_vote == 2:
                            #order: ppc, liberal, green
                            current_green_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ppc, liberal, green, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, liberal, green, conservative, ndp, bloc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: ppc, liberal, green, conservative, bloc, ndp
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ppc, liberal, green, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, liberal, green, ndp, conservative, bloc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ppc, liberal, green, ndp, bloc, conservative
                                    current_bloc_score += 1
                            
                            else:
                                #order: ppc, liberal, green, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, liberal, green, bloc, conservative, ndp
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ppc, liberal, green, bloc, ndp, conservative
                                    current_ndp_score += 1
                        
                        else:
                            #order: ppc, liberal, bloc
                            current_bloc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ppc, liberal, bloc, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, liberal, bloc, conservative, ndp, green
                                    current_ndp_score += 1
                                
                                else:
                                    #order: ppc, liberal, bloc, conservative, green, ndp
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ppc, liberal, bloc, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, liberal, bloc, ndp, conservative, green
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ppc, liberal, bloc, ndp, green, conservative
                                    current_green_score += 1
                            
                            else:
                                #order: ppc, liberal, bloc, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, liberal, bloc, green, conservative, ndp
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ppc, liberal, bloc, green, ndp, conservative
                                    current_ndp_score += 1
                    
                    elif index_of_second_vote == 3:

                        #order: ppc, green
                        current_green_score += 4
                        alpha = np.delete(alpha, index_of_second_vote)
                        index_of_third_vote = next_choice_sim(alpha)

                        if index_of_third_vote == 0:
                            #order: ppc, green, conservative
                            current_conservative_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ppc, green, conservative, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, green, conservative, ndp, liberal, bloc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: ppc, green, conservative, ndp, bloc, liberal
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ppc, green, conservative, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, green, conservative, liberal, ndp, bloc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: ppc, green, conservative, liberal, bloc, ndp
                                    current_bloc_score += 1
                            
                            else:
                                #order: ppc, green, conservative, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, green, conservative, bloc, ndp, liberal
                                    current_ndp_score += 1
                                
                                else:
                                    #order: ppc, green, conservative, bloc, liberal, ndp
                                    current_liberal_score += 1
                        
                        elif index_of_third_vote == 1:
                            #order: ppc, green, ndp
                            current_ndp_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ppc, green, ndp, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, green, ndp, conservative, liberal, bloc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: ppc, green, ndp, conservative, bloc, liberal
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ppc, green, ndp, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, green, ndp, liberal, conservative, bloc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ppc, green, ndp, liberal, bloc, conservative
                                    current_bloc_score += 1
                            
                            else:
                                #order: ppc, green, ndp, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, green, ndp, bloc, conservative, liberal
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ppc, green, ndp, bloc, liberal, conservative
                                    current_liberal_score += 1

                        elif index_of_third_vote == 2:
                            #order: ppc, green, liberal
                            current_liberal_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ppc, green, liberal, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, green, liberal, conservative, ndp, bloc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: ppc, green, liberal, conservative, bloc, ndp
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ppc, green, liberal, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, green, liberal, ndp, conservative, bloc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ppc, green, liberal, ndp, bloc, conservative
                                    current_bloc_score += 1
                            
                            else:
                                #order: ppc, green, liberal, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, green, liberal, bloc, conservative, ndp
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ppc, green, liberal, bloc, ndp, conservative
                                    current_ndp_score += 1
                        
                        else:
                            #order: ppc, green, bloc
                            current_bloc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ppc, green, bloc, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, green, bloc, conservative, ndp, liberal
                                    current_ndp_score += 1
                                
                                else:
                                    #order: ppc, green, bloc, conservative, liberal, ndp
                                    current_liberal_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ppc, green, bloc, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, green, bloc, ndp, conservative, liberal
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ppc, green, bloc, ndp, liberal, conservative
                                    current_liberal_score += 1
                            
                            else:
                                #order: ppc, green, bloc, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, green, bloc, liberal, conservative, ndp
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ppc, green, bloc, liberal, ndp, conservative
                                    current_ndp_score += 1
                    
                    else:
                        #order: ppc, bloc
                        current_bloc_score += 4
                        alpha = np.delete(alpha, index_of_second_vote)
                        index_of_third_vote = next_choice_sim(alpha)

                        if index_of_third_vote == 0:
                            #order: ppc, bloc, conservative
                            current_conservative_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ppc, bloc, conservative, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, bloc, conservative, ndp, liberal, green
                                    current_liberal_score += 1
                                
                                else:
                                    #order: ppc, bloc, conservative, ndp, green, liberal
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ppc, bloc, conservative, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, bloc, conservative, liberal, ndp, green
                                    current_ndp_score += 1
                                
                                else:
                                    #order: ppc, bloc, conservative, liberal, green, ndp
                                    current_green_score += 1
                            
                            else:
                                #order: ppc, bloc, conservative, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, bloc, conservative, green, ndp, liberal
                                    current_ndp_score += 1
                                
                                else:
                                    #order: ppc, bloc, conservative, green, liberal, ndp
                                    current_liberal_score += 1
                        
                        elif index_of_third_vote == 1:
                            #order: ppc, bloc, ndp
                            current_ndp_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ppc, bloc, ndp, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, bloc, ndp, conservative, liberal, green
                                    current_liberal_score += 1
                                
                                else:
                                    #order: ppc, bloc, ndp, conservative, green, liberal
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ppc, bloc, ndp, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, bloc, ndp, liberal, conservative, green
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ppc, bloc, ndp, liberal, green, conservative
                                    current_green_score += 1
                            
                            else:
                                #order: ppc, bloc, ndp, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, bloc, ndp, green, conservative, liberal
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ppc, bloc, ndp, green, liberal, conservative
                                    current_liberal_score += 1

                        elif index_of_third_vote == 2:
                            #order: ppc, bloc, liberal
                            current_liberal_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ppc, bloc, liberal, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, bloc, liberal, conservative, ndp, green
                                    current_ndp_score += 1
                                
                                else:
                                    #order: ppc, bloc, liberal, conservative, green, ndp
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ppc, bloc, liberal, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, bloc, liberal, ndp, conservative, green
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ppc, bloc, liberal, ndp, green, conservative
                                    current_green_score += 1
                            
                            else:
                                #order: ppc, bloc, liberal, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, bloc, liberal, green, conservative, ndp
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ppc, bloc, liberal, green, ndp, conservative
                                    current_ndp_score += 1
                        
                        else:
                            #order: ppc, bloc, green
                            current_green_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: ppc, bloc, green, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, bloc, green, conservative, ndp, liberal
                                    current_ndp_score += 1
                                
                                else:
                                    #order: ppc, bloc, green, conservative, liberal, ndp
                                    current_liberal_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: ppc, bloc, green, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, bloc, green, ndp, conservative, liberal
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ppc, bloc, green, ndp, liberal, conservative
                                    current_liberal_score += 1
                            
                            else:
                                #order: ppc, bloc, green, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: ppc, bloc, green, liberal, conservative, ndp
                                    current_conservative_score += 1
                                
                                else:
                                    #order: ppc, bloc, green, liberal, ndp, conservative
                                    current_ndp_score += 1

                elif index_of_top_vote == 4:
                    #order: green
                    current_green_score += 5
                    index_of_second_vote = next_choice_sim(alpha)
                    
                    if index_of_second_vote == 0:
                        #order: green, conservative
                        current_conservative_score += 4
                        alpha = np.delete(alpha, index_of_second_vote)
                        index_of_third_vote = next_choice_sim(alpha)

                        if index_of_third_vote == 0:
                            #order: green, conservative, ndp
                            current_ndp_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: green, conservative, ndp, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, conservative, ndp, liberal, ppc, bloc
                                    current_ppc_score += 1
                                
                                else:
                                    #order: green, conservative, ndp, liberal, bloc, ppc
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: green, conservative, ndp, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, conservative, ndp, ppc, liberal, bloc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: green, conservative, ndp, ppc, bloc, liberal
                                    current_bloc_score += 1
                            
                            else:
                                #order: green, conservative, ndp, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, conservative, ndp, bloc, liberal, ppc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: green, conservative, ndp, bloc, ppc, liberal
                                    current_ppc_score += 1
                        
                        elif index_of_third_vote == 1:
                            #order: green, conservative, liberal
                            current_liberal_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: green, conservative, liberal, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, conservative, liberal, ndp, ppc, bloc
                                    current_ppc_score += 1
                                
                                else:
                                    #order: green, conservative, liberal, ndp, bloc, ppc
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: green, conservative, liberal, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, conservative, liberal, ppc, ndp, bloc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: green, conservative, liberal, ppc, bloc, ndp
                                    current_bloc_score += 1
                            
                            else:
                                #order: green, conservative, liberal, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, conservative, liberal, bloc, ndp, ppc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: green, conservative, liberal, bloc, ppc, ndp
                                    current_ppc_score += 1

                        elif index_of_third_vote == 2:
                            #order: green, conservative, ppc
                            current_ppc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: green, conservative, ppc, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, conservative, ppc, ndp, liberal, bloc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: green, conservative, ppc, ndp, bloc, liberal
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: green, conservative, ppc, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, conservative, ppc, liberal, ndp, bloc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: green, conservative, ppc, liberal, bloc, ndp
                                    current_bloc_score += 1
                            
                            else:
                                #order: green, conservative, ppc, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, conservative, ppc, bloc, ndp, liberal
                                    current_ndp_score += 1
                                
                                else:
                                    #order: green, conservative, ppc, bloc, liberal, ndp
                                    current_liberal_score += 1
                        
                        else:
                            #order: green, conservative, bloc
                            current_bloc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: green, conservative, bloc, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, conservative, bloc, ndp, liberal, ppc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: green, conservative, bloc, ndp, ppc, liberal
                                    current_ppc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: green, conservative, bloc, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, conservative, bloc, liberal, ndp, ppc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: green, conservative, bloc, liberal, ppc, ndp
                                    current_ppc_score += 1
                            
                            else:
                                #order: green, conservative, bloc, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, conservative, bloc, ppc, ndp, liberal
                                    current_ndp_score += 1
                                
                                else:
                                    #order: green, conservative, bloc, ppc, liberal, ndp
                                    current_liberal_score += 1

                    elif index_of_second_vote == 1:
                        #order: green, ndp
                        current_ndp_score += 4
                        alpha = np.delete(alpha, index_of_second_vote)
                        index_of_third_vote = next_choice_sim(alpha)

                        if index_of_third_vote == 0:
                            #order: green, ndp, conservative
                            current_conservative_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: green, ndp, conservative, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, ndp, conservative, liberal, ppc, bloc
                                    current_ppc_score += 1
                                
                                else:
                                    #order: green, ndp, conservative, liberal, bloc, ppc
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: green, ndp, conservative, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, ndp, conservative, ppc, liberal, bloc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: green, ndp, conservative, ppc, bloc, liberal
                                    current_bloc_score += 1
                            
                            else:
                                #order: green, ndp, conservative, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, ndp, conservative, bloc, liberal, ppc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: green, ndp, conservative, bloc, ppc, liberal
                                    current_ppc_score += 1
                        
                        elif index_of_third_vote == 1:
                            #order: green, ndp, liberal
                            current_liberal_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: green, ndp, liberal, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, ndp, liberal, conservative, ppc, bloc
                                    current_ppc_score += 1
                                
                                else:
                                    #order: green, ndp, liberal, conservative, bloc, ppc
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: green, ndp, liberal, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, ndp, liberal, ppc, conservative, bloc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: green, ndp, liberal, ppc, bloc, conservative
                                    current_bloc_score += 1
                            
                            else:
                                #order: green, ndp, liberal, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, ndp, liberal, bloc, conservative, ppc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: green, ndp, liberal, bloc, ppc, conservative
                                    current_ppc_score += 1

                        elif index_of_third_vote == 2:
                            #order: green, ndp, ppc
                            current_ppc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: green, ndp, ppc, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, ndp, ppc, conservative, liberal, bloc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: green, ndp, ppc, conservative, bloc, liberal
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: green, ndp, ppc, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, ndp, ppc, liberal, conservative, bloc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: green, ndp, ppc, liberal, bloc, conservative
                                    current_bloc_score += 1
                            
                            else:
                                #order: green, ndp, ppc, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, ndp, ppc, bloc, conservative, liberal
                                    current_conservative_score += 1
                                
                                else:
                                    #order: green, ndp, ppc, bloc, liberal, conservative
                                    current_liberal_score += 1
                        
                        else:
                            #order: green, ndp, bloc
                            current_bloc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: green, ndp, bloc, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, ndp, bloc, conservative, liberal, ppc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: green, ndp, bloc, conservative, ppc, liberal
                                    current_ppc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: green, ndp, bloc, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, ndp, bloc, liberal, conservative, ppc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: green, ndp, bloc, liberal, ppc, conservative
                                    current_ppc_score += 1
                            
                            else:
                                #order: green, ndp, bloc, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, ndp, bloc, ppc, conservative, liberal
                                    current_conservative_score += 1
                                
                                else:
                                    #order: green, ndp, bloc, ppc, liberal, conservative
                                    current_liberal_score += 1
                    
                    elif index_of_second_vote == 2:
                        #order: green, liberal
                        current_liberal_score += 4
                        alpha = np.delete(alpha, index_of_second_vote)
                        index_of_third_vote = next_choice_sim(alpha)

                        if index_of_third_vote == 0:
                            #order: green, liberal, conservative
                            current_conservative_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: green, liberal, conservative, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, liberal, conservative, ndp, ppc, bloc
                                    current_ppc_score += 1
                                
                                else:
                                    #order: green, liberal, conservative, ndp, bloc, ppc
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: green, liberal, conservative, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, liberal, conservative, ppc, ndp, bloc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: green, liberal, conservative, ppc, bloc, ndp
                                    current_bloc_score += 1
                            
                            else:
                                #order: green, liberal, conservative, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, liberal, conservative, bloc, ndp, ppc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: green, liberal, conservative, bloc, ppc, ndp
                                    current_ppc_score += 1
                        
                        elif index_of_third_vote == 1:
                            #order: green, liberal, ndp
                            current_ndp_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: green, liberal, ndp, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, liberal, ndp, conservative, ppc, bloc
                                    current_ppc_score += 1
                                
                                else:
                                    #order: green, liberal, ndp, conservative, bloc, ppc
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: green, liberal, ndp, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, liberal, ndp, ppc, conservative, bloc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: green, liberal, ndp, ppc, bloc, conservative
                                    current_bloc_score += 1
                            
                            else:
                                #order: green, liberal, ndp, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, liberal, ndp, bloc, conservative, ppc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: green, liberal, ndp, bloc, ppc, conservative
                                    current_ppc_score += 1

                        elif index_of_third_vote == 2:
                            #order: green, liberal, ppc
                            current_ppc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: green, liberal, ppc, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, liberal, ppc, conservative, ndp, bloc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: green, liberal, ppc, conservative, bloc, ndp
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: green, liberal, ppc, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, liberal, ppc, ndp, conservative, bloc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: green, liberal, ppc, ndp, bloc, conservative
                                    current_bloc_score += 1
                            
                            else:
                                #order: green, liberal, ppc, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, liberal, ppc, bloc, conservative, ndp
                                    current_conservative_score += 1
                                
                                else:
                                    #order: green, liberal, ppc, bloc, ndp, conservative
                                    current_ndp_score += 1
                        
                        else:
                            #order: green, liberal, bloc
                            current_bloc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: green, liberal, bloc, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, liberal, bloc, conservative, ndp, ppc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: green, liberal, bloc, conservative, ppc, ndp
                                    current_ppc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: green, liberal, bloc, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, liberal, bloc, ndp, conservative, ppc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: green, liberal, bloc, ndp, ppc, conservative
                                    current_ppc_score += 1
                            
                            else:
                                #order: green, liberal, bloc, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, liberal, bloc, ppc, conservative, ndp
                                    current_conservative_score += 1
                                
                                else:
                                    #order: green, liberal, bloc, ppc, ndp, conservative
                                    current_ndp_score += 1
                    
                    elif index_of_second_vote == 3:

                        #order: green, ppc
                        current_ppc_score += 4
                        alpha = np.delete(alpha, index_of_second_vote)
                        index_of_third_vote = next_choice_sim(alpha)

                        if index_of_third_vote == 0:
                            #order: green, ppc, conservative
                            current_conservative_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: green, ppc, conservative, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, ppc, conservative, ndp, liberal, bloc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: green, ppc, conservative, ndp, bloc, liberal
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: green, ppc, conservative, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, ppc, conservative, liberal, ndp, bloc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: green, ppc, conservative, liberal, bloc, ndp
                                    current_bloc_score += 1
                            
                            else:
                                #order: green, ppc, conservative, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, ppc, conservative, bloc, ndp, liberal
                                    current_ndp_score += 1
                                
                                else:
                                    #order: green, ppc, conservative, bloc, liberal, ndp
                                    current_liberal_score += 1
                        
                        elif index_of_third_vote == 1:
                            #order: green, ppc, ndp
                            current_ndp_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: green, ppc, ndp, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, ppc, ndp, conservative, liberal, bloc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: green, ppc, ndp, conservative, bloc, liberal
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: green, ppc, ndp, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, ppc, ndp, liberal, conservative, bloc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: green, ppc, ndp, liberal, bloc, conservative
                                    current_bloc_score += 1
                            
                            else:
                                #order: green, ppc, ndp, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, ppc, ndp, bloc, conservative, liberal
                                    current_conservative_score += 1
                                
                                else:
                                    #order: green, ppc, ndp, bloc, liberal, conservative
                                    current_liberal_score += 1

                        elif index_of_third_vote == 2:
                            #order: green, ppc, liberal
                            current_liberal_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: green, ppc, liberal, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, ppc, liberal, conservative, ndp, bloc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: green, ppc, liberal, conservative, bloc, ndp
                                    current_bloc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: green, ppc, liberal, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, ppc, liberal, ndp, conservative, bloc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: green, ppc, liberal, ndp, bloc, conservative
                                    current_bloc_score += 1
                            
                            else:
                                #order: green, ppc, liberal, bloc
                                current_bloc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, ppc, liberal, bloc, conservative, ndp
                                    current_conservative_score += 1
                                
                                else:
                                    #order: green, ppc, liberal, bloc, ndp, conservative
                                    current_ndp_score += 1
                        
                        else:
                            #order: green, ppc, bloc
                            current_bloc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: green, ppc, bloc, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, ppc, bloc, conservative, ndp, liberal
                                    current_ndp_score += 1
                                
                                else:
                                    #order: green, ppc, bloc, conservative, liberal, ndp
                                    current_liberal_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: green, ppc, bloc, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, ppc, bloc, ndp, conservative, liberal
                                    current_conservative_score += 1
                                
                                else:
                                    #order: green, ppc, bloc, ndp, liberal, conservative
                                    current_liberal_score += 1
                            
                            else:
                                #order: green, ppc, bloc, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, ppc, bloc, liberal, conservative, ndp
                                    current_conservative_score += 1
                                
                                else:
                                    #order: green, ppc, bloc, liberal, ndp, conservative
                                    current_ndp_score += 1
                    
                    else:
                        #order: green, bloc
                        current_bloc_score += 4
                        alpha = np.delete(alpha, index_of_second_vote)
                        index_of_third_vote = next_choice_sim(alpha)

                        if index_of_third_vote == 0:
                            #order: green, bloc, conservative
                            current_conservative_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: green, bloc, conservative, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, bloc, conservative, ndp, liberal, ppc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: green, bloc, conservative, ndp, ppc, liberal
                                    current_ppc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: green, bloc, conservative, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, bloc, conservative, liberal, ndp, ppc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: green, bloc, conservative, liberal, ppc, ndp
                                    current_ppc_score += 1
                            
                            else:
                                #order: green, bloc, conservative, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, bloc, conservative, ppc, ndp, liberal
                                    current_ndp_score += 1
                                
                                else:
                                    #order: green, bloc, conservative, ppc, liberal, ndp
                                    current_liberal_score += 1
                        
                        elif index_of_third_vote == 1:
                            #order: green, bloc, ndp
                            current_ndp_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: green, bloc, ndp, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, bloc, ndp, conservative, liberal, ppc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: green, bloc, ndp, conservative, ppc, liberal
                                    current_ppc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: green, bloc, ndp, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, bloc, ndp, liberal, conservative, ppc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: green, bloc, ndp, liberal, ppc, conservative
                                    current_ppc_score += 1
                            
                            else:
                                #order: green, bloc, ndp, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, bloc, ndp, ppc, conservative, liberal
                                    current_conservative_score += 1
                                
                                else:
                                    #order: green, bloc, ndp, ppc, liberal, conservative
                                    current_liberal_score += 1

                        elif index_of_third_vote == 2:
                            #order: green, bloc, liberal
                            current_liberal_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: green, bloc, liberal, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, bloc, liberal, conservative, ndp, ppc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: green, bloc, liberal, conservative, ppc, ndp
                                    current_ppc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: green, bloc, liberal, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, bloc, liberal, ndp, conservative, ppc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: green, bloc, liberal, ndp, ppc, conservative
                                    current_ppc_score += 1
                            
                            else:
                                #order: green, bloc, liberal, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, bloc, liberal, ppc, conservative, ndp
                                    current_conservative_score += 1
                                
                                else:
                                    #order: green, bloc, liberal, ppc, ndp, conservative
                                    current_ndp_score += 1
                        
                        else:
                            #order: green, bloc, ppc
                            current_ppc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: green, bloc, ppc, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, bloc, ppc, conservative, ndp, liberal
                                    current_ndp_score += 1
                                
                                else:
                                    #order: green, bloc, ppc, conservative, liberal, ndp
                                    current_liberal_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: green, bloc, ppc, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, bloc, ppc, ndp, conservative, liberal
                                    current_conservative_score += 1
                                
                                else:
                                    #order: green, bloc, ppc, ndp, liberal, conservative
                                    current_liberal_score += 1
                            
                            else:
                                #order: green, bloc, ppc, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: green, bloc, ppc, liberal, conservative, ndp
                                    current_conservative_score += 1
                                
                                else:
                                    #order: green, bloc, ppc, liberal, ndp, conservative
                                    current_ndp_score += 1

                else:
                    #order: bloc
                    current_bloc_score += 5
                    index_of_second_vote = next_choice_sim(alpha)
                    
                    if index_of_second_vote == 0:
                        #order: bloc, conservative
                        current_conservative_score += 4
                        alpha = np.delete(alpha, index_of_second_vote)
                        index_of_third_vote = next_choice_sim(alpha)

                        if index_of_third_vote == 0:
                            #order: bloc, conservative, ndp
                            current_ndp_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: bloc, conservative, ndp, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, conservative, ndp, liberal, ppc, green
                                    current_ppc_score += 1
                                
                                else:
                                    #order: bloc, conservative, ndp, liberal, green, ppc
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: bloc, conservative, ndp, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, conservative, ndp, ppc, liberal, green
                                    current_liberal_score += 1
                                
                                else:
                                    #order: bloc, conservative, ndp, ppc, green, liberal
                                    current_green_score += 1
                            
                            else:
                                #order: bloc, conservative, ndp, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, conservative, ndp, green, liberal, ppc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: bloc, conservative, ndp, green, ppc, liberal
                                    current_ppc_score += 1
                        
                        elif index_of_third_vote == 1:
                            #order: bloc, conservative, liberal
                            current_liberal_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: bloc, conservative, liberal, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, conservative, liberal, ndp, ppc, green
                                    current_ppc_score += 1
                                
                                else:
                                    #order: bloc, conservative, liberal, ndp, green, ppc
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: bloc, conservative, liberal, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, conservative, liberal, ppc, ndp, green
                                    current_ndp_score += 1
                                
                                else:
                                    #order: bloc, conservative, liberal, ppc, green, ndp
                                    current_green_score += 1
                            
                            else:
                                #order: bloc, conservative, liberal, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, conservative, liberal, green, ndp, ppc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: bloc, conservative, liberal, green, ppc, ndp
                                    current_ppc_score += 1

                        elif index_of_third_vote == 2:
                            #order: bloc, conservative, ppc
                            current_ppc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: bloc, conservative, ppc, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, conservative, ppc, ndp, liberal, green
                                    current_liberal_score += 1
                                
                                else:
                                    #order: bloc, conservative, ppc, ndp, green, liberal
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: bloc, conservative, ppc, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, conservative, ppc, liberal, ndp, green
                                    current_ndp_score += 1
                                
                                else:
                                    #order: bloc, conservative, ppc, liberal, green, ndp
                                    current_green_score += 1
                            
                            else:
                                #order: bloc, conservative, ppc, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, conservative, ppc, green, ndp, liberal
                                    current_ndp_score += 1
                                
                                else:
                                    #order: bloc, conservative, ppc, green, liberal, ndp
                                    current_liberal_score += 1
                        
                        else:
                            #order: bloc, conservative, green
                            current_green_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: bloc, conservative, green, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, conservative, green, ndp, liberal, ppc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: bloc, conservative, green, ndp, ppc, liberal
                                    current_ppc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: bloc, conservative, green, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, conservative, green, liberal, ndp, ppc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: bloc, conservative, green, liberal, ppc, ndp
                                    current_ppc_score += 1
                            
                            else:
                                #order: bloc, conservative, green, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, conservative, green, ppc, ndp, liberal
                                    current_ndp_score += 1
                                
                                else:
                                    #order: bloc, conservative, green, ppc, liberal, ndp
                                    current_liberal_score += 1

                    elif index_of_second_vote == 1:
                        #order: bloc, ndp
                        current_ndp_score += 4
                        alpha = np.delete(alpha, index_of_second_vote)
                        index_of_third_vote = next_choice_sim(alpha)

                        if index_of_third_vote == 0:
                            #order: bloc, ndp, conservative
                            current_conservative_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: bloc, ndp, conservative, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, ndp, conservative, liberal, ppc, green
                                    current_ppc_score += 1
                                
                                else:
                                    #order: bloc, ndp, conservative, liberal, green, ppc
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: bloc, ndp, conservative, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, ndp, conservative, ppc, liberal, green
                                    current_liberal_score += 1
                                
                                else:
                                    #order: bloc, ndp, conservative, ppc, green, liberal
                                    current_green_score += 1
                            
                            else:
                                #order: bloc, ndp, conservative, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, ndp, conservative, green, liberal, ppc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: bloc, ndp, conservative, green, ppc, liberal
                                    current_ppc_score += 1
                        
                        elif index_of_third_vote == 1:
                            #order: bloc, ndp, liberal
                            current_liberal_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: bloc, ndp, liberal, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, ndp, liberal, conservative, ppc, green
                                    current_ppc_score += 1
                                
                                else:
                                    #order: bloc, ndp, liberal, conservative, green, ppc
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: bloc, ndp, liberal, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, ndp, liberal, ppc, conservative, green
                                    current_conservative_score += 1
                                
                                else:
                                    #order: bloc, ndp, liberal, ppc, green, conservative
                                    current_green_score += 1
                            
                            else:
                                #order: bloc, ndp, liberal, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, ndp, liberal, green, conservative, ppc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: bloc, ndp, liberal, green, ppc, conservative
                                    current_ppc_score += 1

                        elif index_of_third_vote == 2:
                            #order: bloc, ndp, ppc
                            current_ppc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: bloc, ndp, ppc, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, ndp, ppc, conservative, liberal, green
                                    current_liberal_score += 1
                                
                                else:
                                    #order: bloc, ndp, ppc, conservative, green, liberal
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: bloc, ndp, ppc, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, ndp, ppc, liberal, conservative, green
                                    current_conservative_score += 1
                                
                                else:
                                    #order: bloc, ndp, ppc, liberal, green, conservative
                                    current_green_score += 1
                            
                            else:
                                #order: bloc, ndp, ppc, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, ndp, ppc, green, conservative, liberal
                                    current_conservative_score += 1
                                
                                else:
                                    #order: bloc, ndp, ppc, green, liberal, conservative
                                    current_liberal_score += 1
                        
                        else:
                            #order: bloc, ndp, green
                            current_green_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: bloc, ndp, green, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, ndp, green, conservative, liberal, ppc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: bloc, ndp, green, conservative, ppc, liberal
                                    current_ppc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: bloc, ndp, green, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, ndp, green, liberal, conservative, ppc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: bloc, ndp, green, liberal, ppc, conservative
                                    current_ppc_score += 1
                            
                            else:
                                #order: bloc, ndp, green, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, ndp, green, ppc, conservative, liberal
                                    current_conservative_score += 1
                                
                                else:
                                    #order: bloc, ndp, green, ppc, liberal, conservative
                                    current_liberal_score += 1
                    
                    elif index_of_second_vote == 2:
                        #order: bloc, liberal
                        current_liberal_score += 4
                        alpha = np.delete(alpha, index_of_second_vote)
                        index_of_third_vote = next_choice_sim(alpha)

                        if index_of_third_vote == 0:
                            #order: bloc, liberal, conservative
                            current_conservative_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: bloc, liberal, conservative, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, liberal, conservative, ndp, ppc, green
                                    current_ppc_score += 1
                                
                                else:
                                    #order: bloc, liberal, conservative, ndp, green, ppc
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: bloc, liberal, conservative, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, liberal, conservative, ppc, ndp, green
                                    current_ndp_score += 1
                                
                                else:
                                    #order: bloc, liberal, conservative, ppc, green, ndp
                                    current_green_score += 1
                            
                            else:
                                #order: bloc, liberal, conservative, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, liberal, conservative, green, ndp, ppc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: bloc, liberal, conservative, green, ppc, ndp
                                    current_ppc_score += 1
                        
                        elif index_of_third_vote == 1:
                            #order: bloc, liberal, ndp
                            current_ndp_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: bloc, liberal, ndp, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, liberal, ndp, conservative, ppc, green
                                    current_ppc_score += 1
                                
                                else:
                                    #order: bloc, liberal, ndp, conservative, green, ppc
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: bloc, liberal, ndp, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, liberal, ndp, ppc, conservative, green
                                    current_conservative_score += 1
                                
                                else:
                                    #order: bloc, liberal, ndp, ppc, green, conservative
                                    current_green_score += 1
                            
                            else:
                                #order: bloc, liberal, ndp, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, liberal, ndp, green, conservative, ppc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: bloc, liberal, ndp, green, ppc, conservative
                                    current_ppc_score += 1

                        elif index_of_third_vote == 2:
                            #order: bloc, liberal, ppc
                            current_ppc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: bloc, liberal, ppc, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, liberal, ppc, conservative, ndp, green
                                    current_ndp_score += 1
                                
                                else:
                                    #order: bloc, liberal, ppc, conservative, green, ndp
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: bloc, liberal, ppc, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, liberal, ppc, ndp, conservative, green
                                    current_conservative_score += 1
                                
                                else:
                                    #order: bloc, liberal, ppc, ndp, green, conservative
                                    current_green_score += 1
                            
                            else:
                                #order: bloc, liberal, ppc, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, liberal, ppc, green, conservative, ndp
                                    current_conservative_score += 1
                                
                                else:
                                    #order: bloc, liberal, ppc, green, ndp, conservative
                                    current_ndp_score += 1
                        
                        else:
                            #order: bloc, liberal, green
                            current_green_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: bloc, liberal, green, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, liberal, green, conservative, ndp, ppc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: bloc, liberal, green, conservative, ppc, ndp
                                    current_ppc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: bloc, liberal, green, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, liberal, green, ndp, conservative, ppc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: bloc, liberal, green, ndp, ppc, conservative
                                    current_ppc_score += 1
                            
                            else:
                                #order: bloc, liberal, green, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, liberal, green, ppc, conservative, ndp
                                    current_conservative_score += 1
                                
                                else:
                                    #order: bloc, liberal, green, ppc, ndp, conservative
                                    current_ndp_score += 1
                    
                    elif index_of_second_vote == 3:

                        #order: bloc, ppc
                        current_ppc_score += 4
                        alpha = np.delete(alpha, index_of_second_vote)
                        index_of_third_vote = next_choice_sim(alpha)

                        if index_of_third_vote == 0:
                            #order: bloc, ppc, conservative
                            current_conservative_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: bloc, ppc, conservative, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, ppc, conservative, ndp, liberal, green
                                    current_liberal_score += 1
                                
                                else:
                                    #order: bloc, ppc, conservative, ndp, green, liberal
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: bloc, ppc, conservative, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, ppc, conservative, liberal, ndp, green
                                    current_ndp_score += 1
                                
                                else:
                                    #order: bloc, ppc, conservative, liberal, green, ndp
                                    current_green_score += 1
                            
                            else:
                                #order: bloc, ppc, conservative, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, ppc, conservative, green, ndp, liberal
                                    current_ndp_score += 1
                                
                                else:
                                    #order: bloc, ppc, conservative, green, liberal, ndp
                                    current_liberal_score += 1
                        
                        elif index_of_third_vote == 1:
                            #order: bloc, ppc, ndp
                            current_ndp_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: bloc, ppc, ndp, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, ppc, ndp, conservative, liberal, green
                                    current_liberal_score += 1
                                
                                else:
                                    #order: bloc, ppc, ndp, conservative, green, liberal
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: bloc, ppc, ndp, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, ppc, ndp, liberal, conservative, green
                                    current_conservative_score += 1
                                
                                else:
                                    #order: bloc, ppc, ndp, liberal, green, conservative
                                    current_green_score += 1
                            
                            else:
                                #order: bloc, ppc, ndp, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, ppc, ndp, green, conservative, liberal
                                    current_conservative_score += 1
                                
                                else:
                                    #order: bloc, ppc, ndp, green, liberal, conservative
                                    current_liberal_score += 1

                        elif index_of_third_vote == 2:
                            #order: bloc, ppc, liberal
                            current_liberal_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: bloc, ppc, liberal, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, ppc, liberal, conservative, ndp, green
                                    current_ndp_score += 1
                                
                                else:
                                    #order: bloc, ppc, liberal, conservative, green, ndp
                                    current_green_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: bloc, ppc, liberal, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, ppc, liberal, ndp, conservative, green
                                    current_conservative_score += 1
                                
                                else:
                                    #order: bloc, ppc, liberal, ndp, green, conservative
                                    current_green_score += 1
                            
                            else:
                                #order: bloc, ppc, liberal, green
                                current_green_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, ppc, liberal, green, conservative, ndp
                                    current_conservative_score += 1
                                
                                else:
                                    #order: bloc, ppc, liberal, green, ndp, conservative
                                    current_ndp_score += 1
                        
                        else:
                            #order: bloc, ppc, green
                            current_green_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: bloc, ppc, green, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, ppc, green, conservative, ndp, liberal
                                    current_ndp_score += 1
                                
                                else:
                                    #order: bloc, ppc, green, conservative, liberal, ndp
                                    current_liberal_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: bloc, ppc, green, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, ppc, green, ndp, conservative, liberal
                                    current_conservative_score += 1
                                
                                else:
                                    #order: bloc, ppc, green, ndp, liberal, conservative
                                    current_liberal_score += 1
                            
                            else:
                                #order: bloc, ppc, green, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, ppc, green, liberal, conservative, ndp
                                    current_conservative_score += 1
                                
                                else:
                                    #order: bloc, ppc, green, liberal, ndp, conservative
                                    current_ndp_score += 1
                    
                    else:
                        #order: bloc, green
                        current_green_score += 4
                        alpha = np.delete(alpha, index_of_second_vote)
                        index_of_third_vote = next_choice_sim(alpha)

                        if index_of_third_vote == 0:
                            #order: bloc, green, conservative
                            current_conservative_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: bloc, green, conservative, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, green, conservative, ndp, liberal, ppc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: bloc, green, conservative, ndp, ppc, liberal
                                    current_ppc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: bloc, green, conservative, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, green, conservative, liberal, ndp, ppc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: bloc, green, conservative, liberal, ppc, ndp
                                    current_ppc_score += 1
                            
                            else:
                                #order: bloc, green, conservative, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, green, conservative, ppc, ndp, liberal
                                    current_ndp_score += 1
                                
                                else:
                                    #order: bloc, green, conservative, ppc, liberal, ndp
                                    current_liberal_score += 1
                        
                        elif index_of_third_vote == 1:
                            #order: bloc, green, ndp
                            current_ndp_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: bloc, green, ndp, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, green, ndp, conservative, liberal, ppc
                                    current_liberal_score += 1
                                
                                else:
                                    #order: bloc, green, ndp, conservative, ppc, liberal
                                    current_ppc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: bloc, green, ndp, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, green, ndp, liberal, conservative, ppc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: bloc, green, ndp, liberal, ppc, conservative
                                    current_ppc_score += 1
                            
                            else:
                                #order: bloc, green, ndp, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, green, ndp, ppc, conservative, liberal
                                    current_conservative_score += 1
                                
                                else:
                                    #order: bloc, green, ndp, ppc, liberal, conservative
                                    current_liberal_score += 1

                        elif index_of_third_vote == 2:
                            #order: bloc, green, liberal
                            current_liberal_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: bloc, green, liberal, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, green, liberal, conservative, ndp, ppc
                                    current_ndp_score += 1
                                
                                else:
                                    #order: bloc, green, liberal, conservative, ppc, ndp
                                    current_ppc_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: bloc, green, liberal, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, green, liberal, ndp, conservative, ppc
                                    current_conservative_score += 1
                                
                                else:
                                    #order: bloc, green, liberal, ndp, ppc, conservative
                                    current_ppc_score += 1
                            
                            else:
                                #order: bloc, green, liberal, ppc
                                current_ppc_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, green, liberal, ppc, conservative, ndp
                                    current_conservative_score += 1
                                
                                else:
                                    #order: bloc, green, liberal, ppc, ndp, conservative
                                    current_ndp_score += 1
                        
                        else:
                            #order: bloc, green, ppc
                            current_ppc_score += 3
                            alpha = np.delete(alpha, index_of_third_vote)
                            index_of_fourth_vote = next_choice_sim(alpha)

                            if index_of_fourth_vote == 0:
                                #order: bloc, green, ppc, conservative
                                current_conservative_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, green, ppc, conservative, ndp, liberal
                                    current_ndp_score += 1
                                
                                else:
                                    #order: bloc, green, ppc, conservative, liberal, ndp
                                    current_liberal_score += 1
                            
                            elif index_of_fourth_vote == 1:
                                #order: bloc, green, ppc, ndp
                                current_ndp_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, green, ppc, ndp, conservative, liberal
                                    current_conservative_score += 1
                                
                                else:
                                    #order: bloc, green, ppc, ndp, liberal, conservative
                                    current_liberal_score += 1
                            
                            else:
                                #order: bloc, green, ppc, liberal
                                current_liberal_score += 2
                                alpha = np.delete(alpha, index_of_fourth_vote)
                                index_of_fifth_vote = next_choice_sim(alpha)

                                if index_of_fifth_vote == 0:
                                    #order: bloc, green, ppc, liberal, conservative, ndp
                                    current_conservative_score += 1
                                
                                else:
                                    #order: bloc, green, ppc, liberal, ndp, conservative
                                    current_ndp_score += 1

            
            if max([current_conservative_score, current_ndp_score, current_liberal_score, current_ppc_score, current_green_score, current_bloc_score]) == current_conservative_score:
                current_conservative_seats = current_conservative_seats + 1
            elif max([current_conservative_score, current_ndp_score, current_liberal_score, current_ppc_score, current_green_score, current_bloc_score]) == current_ndp_score:
                current_ndp_seats = current_ndp_seats + 1
            elif max([current_conservative_score, current_ndp_score, current_liberal_score, current_ppc_score, current_green_score, current_bloc_score]) == current_liberal_score:
                current_liberal_seats = current_liberal_seats + 1
            elif max([current_conservative_score, current_ndp_score, current_liberal_score, current_ppc_score, current_green_score, current_bloc_score]) == current_ppc_score:
                current_ppc_seats = current_ppc_seats + 1
            elif max([current_conservative_score, current_ndp_score, current_liberal_score, current_ppc_score, current_green_score, current_bloc_score]) == current_green_score:
                current_green_seats = current_green_seats + 1
            else:
                current_bloc_seats = current_bloc_seats + 1

        conservative_scores[i] = current_conservative_seats
        ndp_scores[i] = current_ndp_seats
        liberal_scores[i] = current_liberal_seats
        ppc_scores[i] = current_ppc_seats
        green_scores[i] = current_green_seats
        bloc_scores[i] = current_bloc_seats
    
    array_to_return = [conservative_scores, ndp_scores, liberal_scores, ppc_scores, green_scores, bloc_scores]
    return(array_to_return)
