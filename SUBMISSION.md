# Submission

Fork URL: <!-- paste the URL of your fork here -->

## Files to commit

- [ ] `analyze.sh` and `alert.sh`: your two scripts, committed to the repo

## Questions

Answer in your own words. Where a question asks for output, paste it in a code block.

### Q1. Tell the story of the night in 5-8 lines: when did the outage start and end, which endpoint failed, and what was the peak minute? Back every claim with the command that produced it.

**Your answer:**

<!-- replace this line with your answer -->

### Q2. Which IP is scraping Clipstr and how do you know it is a bot and not a busy customer? Which IP is attacking the admin login and what evidence shows it?

**Your answer:**

<!-- replace this line with your answer -->

### Q3. Paste your `analyze.sh` output for the log. Which one pipeline in the script are you proudest of, and why does `sort | uniq -c | sort -rn` appear so often?

**Your answer:**

<!-- replace this line with your answer -->

### Q4. What exit code does `alert.sh` use and why does that matter to a cron job or a CI pipeline? What threshold would you choose for production and why?

**Your answer:**

<!-- replace this line with your answer -->

### Q5. What would you change to run this on a log that is 50 GB instead of 5 MB?

**Your answer:**

<!-- replace this line with your answer -->

### Q6. Paste the output of `./verify.sh`. It must end with **ALL CHECKS PASSED**.

**Your answer:**

<!-- replace this line with your answer -->

### Q7. **Tear down.** Paste the output of `./verify-teardown.sh`. It must end with **TEARDOWN VERIFIED**.

**Your answer:**

<!-- replace this line with your answer -->
