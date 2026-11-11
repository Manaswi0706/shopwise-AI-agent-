# ShopWise AI Agent 🛒

## About the Project

ShopWise AI Agent is an AI-powered shopping assistant designed to help users find suitable products based on their preferences, budget, and requirements.

The project aims to make product selection easier through product recommendations, ranking, and compatibility checking.

## Key Features

- **Personalized Product Recommendations:** Suggests products based on user preferences.
- **Product Ranking:** Ranks products according to budget, RAM, battery capacity, brand preference, and customer ratings.
- **Budget Filtering:** Filters products according to the user's maximum budget.
- **Compatibility Checking:** Checks whether two products are compatible using available compatibility records.
- **AI-Powered Assistance:** Helps users make informed shopping decisions.

*Note: Features will be updated as the team completes and integrates each module.*

## Technologies Used

- Python
- Git and GitHub
- Google Gemini API (if used in the final implementation)

## Project Structure

```text
shopwise-AI-agent/
│
├── recommendation/
│   ├── __init__.py
│   ├── ranking.py
│   └── compatibility.py
│
├── tests/
│   ├── test_ranking.py
│   └── test_compatibility.py
│
└── .gitignore
```

*Additional folders and files will be added as the other team modules are integrated.*

## Team Contributions

| Team Member | Responsibility |
|---|---|
| Person 1 | AI Agent and User Interaction |
| Person 2 | Product Database and Data Management |
| Person 3 | Product Recommendation, Ranking and Compatibility |
| Person 4 | User Interface and Integration |

## Running the Tests

1. Clone the repository:

```bash
git clone https://github.com/Manaswi0706/shopwise-AI-agent-.git
```

2. Navigate to the project directory:

```bash
cd shopwise-AI-agent
```

3. Install pytest:

```bash
pip install pytest
```

4. Run the tests:

```bash
python -m pytest -v
```

## Current Development Status

The project is being developed collaboratively by a team of four members. Individual modules are developed on separate Git branches and integrated through GitHub Pull Requests.

## Future Improvements

- Improve recommendation accuracy.
- Expand the product database.
- Add more product categories.
- Enhance product compatibility checking.
- Improve the overall shopping experience.

## License

This project is developed for educational and hackathon purposes.
