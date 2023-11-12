import pandas as pd
import numpy as np
import random 
import copy
import math
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

    print("")
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


# Simulated annealing function
def simulated_annealing(df, solution, temperature, cooling_rate, iterations_per_temp):
    """
    arguments: 
        df = dataframe of production times, deadlines & costs  
        solution = dictionary of an initial line production solution 
        temperature = initial temperature 
        cooling_rate = value lower than 1 showing the rate at which the temperature cools
        interations_per_temp = how many times you iterate at a given temperature 

    outputs: 
        best_solution = solution achieved through simulated annealing algorithm
    """
    current_schedule = copy.deepcopy(solution)
    best_solution = copy.deepcopy(solution)
    current_cost = calculate_penalty_cost(df, current_schedule)
    best_cost = current_cost

    while temperature > 0.1:
        for k in range(iterations_per_temp):
            # Generate a neighboring solution by swapping two random cities
            i, j = random.sample(list(current_schedule.keys()), 2)

            # Use indexing to find items in the random lines and replace them in the original dictionary
            item_index_i = random.randint(0, len(current_schedule[i]) - 1)
            item_index_j = random.randint(0, len(current_schedule[j]) - 1)

            # Swap the items
            neighbor_schedule = copy.deepcopy(current_schedule)
            neighbor_schedule[i][item_index_i], neighbor_schedule[j][item_index_j] = neighbor_schedule[j][item_index_j], neighbor_schedule[i][item_index_i]
 
            #neighbor_schedule = current_schedule[:]
            neighbor_cost = calculate_penalty_cost(df, neighbor_schedule)

            # Decide whether to accept the neighbor solution
            delta = neighbor_cost - current_cost
            if delta < 0 or random.random() < 2.7182**(-delta / temperature):
                current_schedule = neighbor_schedule
                current_cost = neighbor_cost

                # Update the best solution if necessary
                if current_cost < best_cost:
                    best_solution = current_schedule
                    best_cost = current_cost

        # Cool the temperature
        temperature *= cooling_rate


    print("Initial Solution:")
    for line, products in solution.items():
        print(f"{line}: {', '.join(products)}")
    print("Initial Penalty Cost:", calculate_penalty_cost(df, solution))

    print("")

    print("Final Best Solution:")
    for line, products in best_solution.items():
        print(f"{line}: {', '.join(products)}")
    print("Final Best Penalty Cost:", best_cost)

    return best_solution

# df=pd.read_excel('Line Production December 2023.xlsx')

# ch = constructive_heuristic_random(df)
# print('Constructive search', ch)
# print('')

# ips = improving_search(20, df, ch)
# print('Improving search', ips)
# print('')

# sa = simulated_annealing(df, ips, 10, 0.99, 10)
# print('Simulated annealing', sa)


#export solution to excel 
def solution_excel(df, solution):
    """
    Arguments: 
        df = dataframe of production times, deadlines & costs  
        solution = dictionary of a solution

    Output:
        excel file of schedule with 8 columns: Product, Line, 
        Start, Process Time, End, Deadline, Tardiness,Total Penalty Cost. 
    
    """
    # Create a new DataFrame with the required columns
    result_data = []

    # Populate the DataFrame with the relevant data
    for line, products in solution.items():
        current_time = 0
        for product in products:
            product_row = df[df['Product'] == product]
            processing_time = product_row[line].values[0]
            deadline = product_row['deadline'].values[0]
            lateness = current_time + processing_time - deadline
            cost_penalty = product_row['penalty cost'].values[0]
            total_penalty_cost = max(0, lateness) * product_row['penalty cost'].values[0]

            result_data.append({
                "Product": product,
                "Line": line,
                "Start": current_time,
                "Process Time": processing_time,
                "End": current_time + processing_time,
                "Deadline": deadline,
                "Tardiness": max(0, lateness),
                "Penalty Cost Per Hour": cost_penalty, 
                "Total Penalty Cost": total_penalty_cost
            })

            current_time += processing_time

    # Convert the list of dictionaries to a DataFrame
    result_df = pd.DataFrame(result_data)
    #.to_excel("OR5: Final Schedule Month 2023")

    return result_df