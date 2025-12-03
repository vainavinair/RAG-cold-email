I have a plan in mind but building on the fly here.
### So far what ive done is:
1. Loaded resume and jobs data(dummy data, might scrappe real data later?)
2. Created chunking embeddings for both resume and job descriptions
3. Ranked jobs based on similarity to resume
4. Generated email content for the top ranked job, and sent email using yagmail

### Next steps:
1. Need to modularize the code
2. Add error handling and logging
3. Go with the scrapping data? or use some API to get real job data
4. Add more data sources fo user context like linkedin profile, portfolio website, user preferences etc.
5. Prompt better, maybe use few shot prompting for email generation

Will update as I progress. Feel free to suggest improvements or point out any issues. Hopefully this will turn into a tool for automating cold job applications and get me some interviews, lol.