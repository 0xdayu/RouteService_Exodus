struct Query
{
    1: required string relName,
    2: required list<string> arguments
}

struct QueryReply
{
    1: required list<list<string>> result,
    2: optional string exception_code,
    3: optional string exception_message
}

struct Notification
{
    1: required string notificationType,
    2: required map<string, string> values
}

service RouteService{
    QueryReply doQuery(1:Query request),
    void notifyMe(1:Notification notify)
}
