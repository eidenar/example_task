### Task limitations:
*   Assumed that there is no middle name case
*   Input and output secrets should be stored in environment variables and 
    parsed on service initialization. But it mainly depends on environment
*   There is no basic validation for each parameter in request. For example length and type for timestamps
---
### Optional part:
*   There is a misconception in this part: from example I can see, that input url is already URL-encoded
    `B02K_CUSTNAME=FIRST%20LAST`, thus non-ascii name "VÄINÖ MÄKI" should be already properly encoded to 
    `"V%C4IN%D6%20M%C4KI"`. Also, output hash is calculated using capitalized first and last name. URL-encoded variant of
    "Väinö Mäki" is `"V%E4in%F6%20M%E4ki"`. So I made a conclusion, that I can calculate hashes using unicode strings and 
    URL-encode links using `windows-1252` encoding