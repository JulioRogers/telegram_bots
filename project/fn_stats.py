import json

def get_statistics():
    # Load the JSON data
    with open('nomoreslavery/datasets/all_data.json') as file:
        data = json.load(file)

    # Extract required information
    countries = {}
    industries = {}
    scores = []

    for entry in data:
        country = entry['country']
        industry = entry['industry']
        score = entry['score']
        scores.append(score)
        
        if country in countries:
            countries[country].append(score)
        else:
            countries[country] = [score]
        
        if industry in industries:
            industries[industry].append(score)
        else:
            industries[industry] = [score]

    # Calculate statistics
    from statistics import mean, stdev

    # Country stats
    country_stats = {country: {"Mean Score": mean(scores), "Count": len(scores)} for country, scores in countries.items()}
    # Industry stats
    industry_stats = {industry: {"Mean Score": mean(scores), "Count": len(scores)} for industry, scores in industries.items()}
    # Overall score stats
    overall_stats = {
        "Total Entries": len(scores),
        "Overall Mean Score": mean(scores),
        "Score Standard Deviation": stdev(scores)
    }
    return country_stats, industry_stats, overall_stats
