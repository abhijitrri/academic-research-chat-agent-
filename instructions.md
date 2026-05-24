# Setup Instructions for AI Research Collaborator Agent

Follow these steps to get the project running on your laptop.

## Step 1: Clone the Repository

Open your terminal and run this command:

```
git clone https://github.com/yourusername/academic-research-chat-agent-.git
```

Then navigate into the project folder:

```
cd academic-research-chat-agent-
```

## Step 2: Create Your Own Branch

Create a new branch with your name or task name. Run this command:

```
git checkout -b your-branch-name
```

Example:
```
git checkout -b dev
```

Or if you want a more descriptive name:
```
git checkout -b feature/my-feature-name
```

## Step 3: Verify You're on the Right Branch

Check which branch you're currently on by running:

```
git status
```

You should see something like: `On branch your-branch-name`

## Step 4: Install Python Dependencies

Run this command to install all required packages:

```
uv sync
```

If you don't have `uv` installed, first install it:
```
pip install uv
```

Then run the sync command again.

## Step 5: Set Up Environment Variables

Create a `.env` file in the project folder with the following content:

```
LLM_PROVIDER=openai
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4
ANTHROPIC_API_KEY=your-anthropic-api-key-here
ANTHROPIC_MODEL=claude-3-sonnet-20240229
DATABASE_URL=postgresql://user:password@localhost:5432/research_db
REDIS_URL=redis://localhost:6379/0
```

Replace:
- `your-openai-api-key-here` with your actual OpenAI API key
- `your-anthropic-api-key-here` with your actual Anthropic API key (if you have one)

## Step 6: Run Streamlit

Start the Streamlit dashboard with this command:

```
uv run streamlit run streamlit_app.py
```

## Step 7: Access the Dashboard

Once the command runs, you'll see output in your terminal. Look for a line that says:

```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
```

Open your web browser and go to:

```
http://localhost:8501
```

The dashboard should now be visible!

## Step 8: Using the Dashboard

1. **Select a Model**: Choose an OpenAI model from the dropdown (gpt-4, gpt-4-turbo, or gpt-3.5-turbo)
2. **Enter a Research Topic**: Type in a research area you want to explore (e.g., "Machine Learning in Healthcare")
3. **Set Parameters**:
   - Number of References: How many papers to find (1-10)
   - Prior Years to Explore: How far back to search (1-50 years)
4. **Click Search**: Click the "🚀 Search" button
5. **View Results**: The dashboard will show:
   - Top Researchers in that field
   - Top Research Papers, Books & Reviews
   - Future Research Directions

## Stopping Streamlit

To stop the Streamlit app, go back to your terminal and press:

```
Ctrl + C
```

## Pushing Your Changes

When you're done working and want to save your changes:

1. Stage your changes:
```
git add .
```

2. Create a commit:
```
git commit -m "Description of what you changed"
```

3. Push to the remote:
```
git push -u origin your-branch-name
```

## Need Help?

If you run into any issues:
- Check that all commands are typed exactly as shown
- Make sure you're in the correct folder (`academic-research-chat-agent-`)
- Verify your API keys are correct in the `.env` file
- Ask your collaborator (the person who gave you these instructions)

---

**That's it! You're all set to start working on the AI Research Collaborator Agent!**
