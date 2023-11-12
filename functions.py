import pandas as pd
import numpy as np
import random 
import copy
random.seed(9)

# # Load data from the file
# if data.endswith('.xlsx'):
#     df = pd.read_excel(data)
# elif data.endswith('.csv'):
#     df = pd.read_csv(data)
# else:
#     raise ValueError("Unsupported file format. Use .xlsx or .csv.")

def calculate_penalty_cost(df, solution):
    """
    arguments: 
        df = dataframe of production times, deadlines & costs 
        solution = dictioanry of line production solution 

    output: total penalty cost of solution given 

    """
    #starting penalty cost value 
    total_penalty_cost = 0

    for line, products in solution.items():

        #initial values 
        line_penalty_cost = 0  
        current_time = 0  

        for product in products:
            #get the data of the specific product that's in the current line 
            product_row = df[df['Product'] == product]

            if not product_row.empty:

                # the products processing time on the line it's being processed on 
                processing_time = product_row[line].values[0]
                # product deadline 
                deadline = product_row['deadline'].values[0]

                # how late the product is 
                lateness = current_time + processing_time - deadline

                #check if the product is late and if yes what the cost is     
                if lateness > 0:
                    penalty_cost = lateness * product_row['penalty cost'].values[0]
                    #add the penalty cost to total cost of that line
                    line_penalty_cost += penalty_cost

                #change current time to that after processing the product 
                current_time += processing_time

        # add penalty cost of everyline together 
        total_penalty_cost += line_penalty_cost

    return total_penalty_cost

#CONSTRUCTIVE HEURISTIC IDEAL LINE ALGORITHM 
def constructive_heuristic_ideal (df): 
    """
    arguments:
        df = dataframe of production times, deadlines & costs  
        
    outputs: 
        best_solution = solution achieved through constructive heuristic ideal line algorithm
    """
    df['proportion']=df['deadline']/df['penalty cost']
    df=df.sort_values(by='proportion')
    df=df.reset_index(drop=True)

    df['ideal line']=''
    line_columns=['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7']
    for product in df.index:
        ideal_line=df[line_columns].idxmin(axis=1)
        df['ideal line']=ideal_line

    df['time on ideal line']=''
    for index in df.index:
        column=df.loc[index, 'ideal line']
        df.loc[index, 'time on ideal line']=df.loc[index, column]
    
    simple_schedule={'L1': [], 'L2': [], 'L3': [], 'L4': [], 'L5': [], 'L6': [], 'L7': []}
    schedule={'L1': [], 'L2': [], 'L3': [], 'L4': [], 'L5': [], 'L6': [], 'L7': []}

    for line in line_columns:
        time=0
        for product in df.index:
            if df.loc[product, 'ideal line']==line:
                time=time+int(df.loc[product, 'time on ideal line'])
                information=[df.loc[product, 'Product'], df.loc[product, 'time on ideal line'], df.loc[product, 'deadline'], time, df.loc[product, 'penalty cost']]
                schedule[line].append(information)
                simple_schedule[line].append(df.loc[product, 'Product'])
                
    total_penalty=0
    for line, sequence in schedule.items():
        #print(f'{line}: {sequence}')
        for product in sequence:
            if product[2]<product[3]:
                #print(product[0], (product[3]-product[2])*product[4])
                total_penalty+=(product[3]-product[2])*product[4]
    
    #name final solution 
    best_solution = simple_schedule
    best_penalty_cost = total_penalty

    print("Final Best Solution:")
    for line, products in best_solution.items():
        print(f"{line}: {', '.join(products)}")
    print("Final Best Penalty Cost:", best_penalty_cost)

    return best_solution 

#CONSTRUCTIVE HEURISTIC RANDOM ALGORITHM
def constructive_heuristic_random(df):
    """
    arguments:
        df = dataframe of production times, deadlines & costs  
        
    outputs: 
        best_solution = solution achieved through constructive heuristic random line algorithm
    """
    df['proportion']=df['deadline']/df['penalty cost']
    df=df.sort_values(by='proportion')
    df=df.reset_index(drop=True)

    df['chosen line']=''
    line_columns=['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7']
    for product in df.index:
        chosen_line=random.choice(line_columns)
        df.loc[product, 'chosen line']=chosen_line

    df['time on chosen line']=''
    for index in df.index:
        column=df.loc[index, 'chosen line']
        df.loc[index, 'time on chosen line']=df.loc[index, column] 

    simple_schedule={'L1': [], 'L2': [], 'L3': [], 'L4': [], 'L5': [], 'L6': [], 'L7': []}
    schedule={'L1': [], 'L2': [], 'L3': [], 'L4': [], 'L5': [], 'L6': [], 'L7': []}

    for line in line_columns:
        time=0
        for product in df.index:
            if df.loc[product, 'chosen line']==line:
                time=time+int(df.loc[product, 'time on chosen line'])
                information=[df.loc[product, 'Product'], df.loc[product, 'time on chosen line'], df.loc[product, 'deadline'], time, df.loc[product, 'penalty cost']]
                schedule[line].append(information)
                simple_schedule[line].append(df.loc[product, 'Product'])

    total_penalty=0
    for line, sequence in schedule.items():
        for product in sequence:
            if product[2]<product[3]:
                total_penalty+=(product[3]-product[2])*product[4]
                
    best_solution = simple_schedule
    best_penalty_cost = total_penalty

    print("Final Best Solution:")
    for line, products in best_solution.items():
        print(f"{line}: {', '.join(products)}")
    print("Final Best Penalty Cost:", best_penalty_cost)

    return best_solution

#IMPROVING SEARCH ALGORITHM
def improving_search(iterations: int, df, solution: dict):
    """
    arguments:
        iterations = integer number of how many swwaps are going to be made 
        df = dataframe of production times, deadlines & costs  
        solution = dictioanry of an initial line production solution 
    
    outputs: 
        best_solution = solution achieved through improving search algorithm
    """

    initial_solution = copy.deepcopy(solution)
    for i in range(iterations):
        # Create a copy of the current initial solution
        best_solution = copy.deepcopy(initial_solution)
        best_penalty_cost = calculate_penalty_cost(df, best_solution)

        #initialize to check if any improvements are made 
        improvement_made = False

        #iterate through every product in every line 
        for line, products in best_solution.items():
            for product in products:
                for line2, target_products in best_solution.items():
                    if line != line2:
                        # create copy and swap through the two copies 
                        new_solution = copy.deepcopy(best_solution)

                        #make sure product is in the first line before swapping to line2
                        if product in new_solution[line]:
                            new_solution[line].remove(product)
                            new_solution[line2].append(product)

                            #new penalty cost after swapping 
                            new_penalty_cost = calculate_penalty_cost(df, new_solution)

                            #is new penalty cost better or worse than older penalty cost
                            if new_penalty_cost < best_penalty_cost:
                                best_solution = copy.deepcopy(new_solution)
                                best_penalty_cost = new_penalty_cost
                                improvement_made = True

        #now check if improvement is made 
        if improvement_made:
            initial_solution = best_solution
        else:
            #no improvement or iterations ran out 
            break

    print("Initial Solution:")
    for line, products in solution.items():
        print(f"{line}: {', '.join(products)}")
    print("Initial Penalty Cost:", calculate_penalty_cost(df, solution))

    print("")

    print("Final Best Solution:")
    for line, products in best_solution.items():
        print(f"{line}: {', '.join(products)}")
    print("Final Best Penalty Cost:", best_penalty_cost)

    return best_solution 