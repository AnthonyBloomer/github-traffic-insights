# github-traffic-insights

> Lambda function to send your [Github traffic statistics](https://developer.github.com/v3/repos/traffic/) to New Relic Insights.

For repositories that you have push access to within Github, the [Github traffic API](https://developer.github.com/v3/repos/traffic/) provides access to the information provided in the [graphs section](https://help.github.com/articles/about-repository-graphs/#traffic) of the repositories UI. 

This information includes referral sources, referral paths, views and clones. The API returns data over the past 14 day period. As the API only returns data over the past 14 day period, this solution aims to give users access to historical Traffic data for their Github repositories within Insights. This Lambda function calls each endpoint every 15 days and creates custom events that you can then query and create visualations within New Relic Insights. 

See the New Relic One Dashboard below:

![Image](https://i.imgur.com/Y6lRjXa.png)

## How it works

The function uses Github's token based API authentication to gain access to the user's repository data. For each of the users repostories, the script makes a call to each Traffic API endpoint and records a custom event using the [Event API](https://docs.newrelic.com/docs/insights/insights-data-sources/custom-data/introduction-event-api) if there has been any Traffic data reported.

## Setup

Clone the repository: `git clone https://github.com/AnthonyBloomer/github-traffic-insights.git`

Update the following environment variables in the `template.yml` file:

- `GITHUB_TOKEN` - Create a personal access token using your [Personal access tokens settings page](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line). 
- `GITHUB_USERNAME` - Your GitHub username.
- `NEW_RELIC_ACCOUNT_ID` - Your New Relic [Account ID](https://docs.newrelic.com/docs/accounts/install-new-relic/account-setup/account-id)
- `NEW_RELIC_INSERT_KEY` - Your New Relic [Insert Key](https://docs.newrelic.com/docs/apis/get-started/intro-apis/types-new-relic-api-keys#event-insert-key)

Deploy using the [AWS CLI](https://aws.amazon.com/cli/):

```
aws cloudformation deploy --template template.yml --stack-name github
```

### Sample Dashboard

The project also includes the [sample dashboard JSON](https://github.com/AnthonyBloomer/github-traffic-insights/blob/master/example_dashboard.json) shown above which you can import into your New Relic account using the [Dashboards API](https://docs.newrelic.com/docs/insights/insights-api/manage-dashboards/insights-dashboard-api).
