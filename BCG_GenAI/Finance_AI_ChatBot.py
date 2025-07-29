import pandas as pd

final_report = pd.read_csv('final_data_report.csv')
summary_report = pd.read_csv('Summary_final_report.csv')

# Creating a basic Rule-based Logic AI-Driven Chatbot
def financial_AI_Chatbot(Data_query):
    
    Data_query = input("\n----Please Enter Your Query-----")

    if Data_query == "Total revenue?":
        revenue = final_report[(final_report['Year'] == Year) & (final_report['Company'] == Company)]['Total Revenue'].values[0]
        return f"The Total Revenue for {Company} for fiscal year {Year} is $ {revenue}"
    
    elif Data_query == "Net Income?":
        net_income  = final_report[(final_report['Year'] == Year) & (final_report['Company'] == Company)]['Net Income'].values[0]
        return f"The Net Income for {Company} for fiscal year {Year} is $ {net_income}"
    
    elif Data_query == "sum of Total assets?":
        Total_assets  = final_report[(final_report['Year'] == Year) & (final_report['Company'] == Company)]['Total Assets'].values[0]
        return f"The sum of Total Assets for {Company} for fiscal year {Year} is $ {Total_assets}"
    
    elif Data_query == "sum of Total liabilities?":
        Total_liabilities  = final_report[(final_report['Year'] == Year) & (final_report['Company'] == Company)]['Total Liabilities'].values[0]
        return f"The sum of Total Liabilities for {Company} for fiscal year {Year} is $ {Total_liabilities}"
    
    elif Data_query == "What's cash flow from operating activities?":
        cash_ops = final_report[(final_report['Year'] == Year) & (final_report['Company'] == Company)]['Cash Flow from Operating Activities'].values[0]
        return f"The Cash Flow from Operating Activities for {Company} for fiscal year {Year} is $ {cash_ops}"
    
    elif Data_query == "revenue growth(%)?":
        revenue_growth = final_report[(final_report['Year'] == Year) & (final_report['Company'] == Company)]['Revenue Growth (%)'].values[0]
        return f"The Revenue Growth(%) for {Company} for fiscal year {Year} is {revenue_growth}(%)"
    
    elif Data_query == "net income growth(%)?":
        net_income_growth = final_report[(final_report['Year'] == Year) & (final_report['Company'] == Company)]['Net Income Growth (%)'].values[0]
        return f"The Net Income Growth(%) for {Company} for fiscal year {Year} is {net_income_growth}(%)"
    
    elif Data_query == "assets growth(%)?":
        assets_growth = final_report[(final_report['Year'] == Year) & (final_report['Company'] == Company)]['Total Assets Growth (%)'].values[0]
        return f"The Assets Growth(%) for {Company} for fiscal year {Year} is {assets_growth}(%)"
    
    elif Data_query == "liabilities growth(%)?":
        liabilities_growth = final_report[(final_report['Year'] == Year) & (final_report['Company'] == Company)]['Liabilities Growth (%)'].values[0]
        return f"The Liabilities Growth(%) for {Company} for fiscal year {Year} is {liabilities_growth}(%)"
    
    elif Data_query == "cash flow from operations growth(%)?":
        cash_ops_growth = final_report[(final_report['Year'] == Year) & (final_report['Company'] == Company)]['Cash Flow from Operations Growth(%)'].values[0]
        return f"The Cash Flow from Operations Growth(%) for {Company} for fiscal year {Year} is {cash_ops_growth}(%)"
    
    elif Data_query == "year by year average revenue growth rate(%)?":
        year_avg_revenue_growth = summary_report[(summary_report['Company'] == Company)]['Revenue Growth (%)'].values[0].round(2)
        return f"The Year By Year - Average Revenue Growth Rate(%) from 2021 to 2023 for {Company} is {year_avg_revenue_growth}(%)"
     
    elif Data_query == "year by year average net income growth rate(%)?":
        year_avg_net_income_growth = summary_report[(summary_report['Company'] == Company)]['Net Income Growth (%)'].values[0].round(3)
        return f"The Year By Year - Net Income Revenue Growth Rate(%) from 2021 to 2023 for {Company} is {year_avg_net_income_growth}(%)"
    
    elif Data_query == "year by year average assets growth rate(%)?":
        year_avg_assets_growth = summary_report[(summary_report['Company'] == Company)]['Total Assets Growth (%)'].values[0].round(2)
        return f"The Year By Year - Average Assets Growth Rate(%) from 2021 to 2023 for {Company} is {year_avg_assets_growth}(%)"
    
    elif Data_query == "year by year average liabilities growth rate(%)?":
        year_avg_liabilities_growth = summary_report[(summary_report['Company'] == Company)]['Liabilities Growth (%)'].values[0].round(2)
        return f"The Year By Year - Average Liabilities Growth Rate(%) from 2021 to 2023 for {Company} is {year_avg_liabilities_growth}(%)"
    
    elif Data_query == "year by year average cash flow from operations growth rate(%)?":
        year_avg_cash_ops_growth = summary_report[(summary_report['Company'] == Company)]['Cash Flow Growth (%)'].values[0].round(2)
        return f"The Year By Year - Average Cash Flow from Operations Growth Rate(%) from 2021 to 2023 for {Company} is {year_avg_cash_ops_growth}(%)" 
    
    else:
        return "Sorry, I can only provide information on the requested query."

# Testing the chatbot
while True:
    print("******************************************************************************")
    user_input = input("\nEnter Hi to start the chatbot session; type 'exit' to quit): ")
    if user_input.lower() == "exit":
        break
    elif user_input.lower() == "hi":
        print("\nHello! Welcome to the AI Driven Financial Chatbot!!!")
        print("\nHey, I can help you with your financial queries")
        print("Please select the company name from the option below: -")
        print("\n1.Microsoft \n2.Tesla \n3.Apple")
        Company = input("Enter company name : ").capitalize()
        if Company not in ['Apple', 'Microsoft', 'Tesla']:
            print("Invalid Company Name. Please check and enter correct company name by starting the chatbot session again")
            break
        else:
            print("\nThe data for the fiscal year - 2023, 2022, and 2021 is currently available.\n")
            Year = int(input("The fiscal year for the selected company : "))
            if Year not in [2023, 2022, 2021]:
                print("\nPlease Enter a valid fiscal year, by starting the chatbot session again")
                break
            
    else:
        print("Enter 'Hi' Properly!!!!! by starting the chatbot session again")
        break        
    response = financial_AI_Chatbot(Data_query=" ")
    print(response)