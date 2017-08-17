# comic-book-data-scraper

Just some quick code I wrote to scrape the comic book sales data on the comichron site and dump it into a database for easy visualization.  I wrote this code to help win an arguement I was having with a friend about whether or not the recent DC and Marvel reboots had a significant impact on sales.

A few notes:
-- The data on comichron is stored in raw HTML tables, and the formatting is inconsistent (i.e. the site uses class tags, but the values associated with each field sometimes changes seemingly arbitrarily).
-- To address the above, I've written in some exceptions to address the weird months (you'll notice some nasty long if statements).
-- I've hardcoded reference to the database output (it's looking for comics.sqlite) out of laziness, but will probably have the program prompt for this in the future.
