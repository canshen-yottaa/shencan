# {x-log-type} {c-ip} {c-username} [{x-localtime}] "{x-request-line}" {cs-bytes} "{sc-status}" {sc-bytes} "{cs-referer}" "{cs-user-agent}" "{x-Yottaa-Optimizations}" "{x-Yottaa-Metrics}" "{sc-content-type}" "{x-forward-for}" {s-domain} [{cs-start-time}] [{cs-end-time}] [{sc-start-time}] [{sc-end-time}] "adnid" protocol prefetch
# C 107.21.76.254 - [02/Apr/2013:02:16:15 +0000] "GET / HTTP/1.1" 180 "200" 443 "-" "YottaaMonitor" "-" "-" "text/html" "50.19.168.191" ready.l09.me 1364868975998 1364868975998 1364868975999 1364868975999 "5153ac1263e31e60fa000640" 0 0
# S 54.236.114.222 - [02/Apr/2013:02:16:15 +0000] "GET / HTTP/1.1" 154 "200" 598 "-" "YottaaMonitor" "ob/1000 si/1714285511 ts/1364777826240 ai/5153ac1263e31e60fa000640" "01216b152448/[9,3,-]" "text/html" "50.19.168.191" ready.l09.me 1364868975993 1364868975993 1364868976003 1364868976003 "-" 0 -
# X-Yottaa-Metrics:node-id/[v2r-time,r2o-time,rInit-time, r2o-retry-1st, r2o-retry-2nd,..], unit is microsecond

BEGIN {
    os_5xx_pattern = " os-5.."
    cs_request = 0
    cs_traffic = 0
    cs_prefetch = 0
    http_request = 0
    http_traffic = 0
    https_request = 0
    https_traffic = 0
    hit = 0
    miss = 0
    status_2xx = 0
    status_3xx = 0
    status_4xx = 0
    status_5xx = 0
    yottaa_status_404 = 0
    yottaa_status_5xx = 0
    os_timeout = 0
    html_response_time = 0  # text/html
    js_response_time = 0  # application/x-javascript
    css_response_time = 0  # text/css
    first_byte = 0
}

function get_cache_status(optimizations,    x, cache_tmp, cache_tmp_length, ob, ob_length, cache_status) {
    cache_tmp_length=split(optimizations, cache_tmp, " ")
    for (x=1; x<=cache_tmp_length; x++) {
        if (match(cache_tmp[x], "^ob/")) {
            ob = cache_tmp[x]
            ob_length = length(ob)
            cache_status = substr(ob, ob_length-1, 1)
            if (cache_status==1) {
               hit++
            } else {
                miss++
            }
            return
        }
    }
    miss++
}

function parse(http_code, request_line, optimizations, metrics,    parse_tmp) {
    if (http_code<300) {
        status_2xx++
    } else if (http_code>=300 && http_code<400) {
        status_3xx++
    } else if (http_code>=400 && http_code<500) {
        status_4xx++
        if (request_line ~ /Y~/) {
            yottaa_status_404++
        }
    } else if (http_code>=500) {
        status_5xx++
        if (match(optimizations, os_5xx_pattern)) {
            split(metrics, parse_tmp, ",")
            if (parse_tmp[2] == "-") os_timeout++
        } else {
            yottaa_status_5xx++
        }
    }
}

function get_response_time(input_fields,    time_array, cs_start_time, cs_end_time, sc_start_time, sc_end_time, response_time) {
    # {s-domain} {cs-start-time} {cs-end-time} {sc-start-time} {sc-end-time}
    # ready.l09.me 1364868975993 1364868975993 1364868976003 1364868976003
    split(input_fields, time_array, " ")
    cs_start_time=time_array[2]
    # cs_end_time=time_array[3]
    sc_start_time=time_array[4]
    sc_end_time=time_array[5]
    first_byte_time = sc_start_time - cs_start_time
    response_time = sc_end_time - sc_start_time
    return response_time
}

{
    # split log entry by double quote
    if (NF!=19) {
        # log entry illegal
        next
    }
    field01 = $1  # {x-log-type} {c-ip} {c-username} [{x-localtime}]
    first_request_line = $2
    # cs_bytes = $3
    sc_status = $4
    sc_bytes = $5
    field19 = $ 19  # protocol prefetch, protocol=1 is https, prefetch=1 is prefetch
    split(field19, a, " ")
    protocol = a[1]
    prefetch = a[2]
    if (match(field01, "^C")) {
        # TPU is client
        cs_request++
        cs_traffic += sc_bytes
        if (prefetch == 1) {
            cs_prefetch++
        }
        next
    }
    if (protocol==0) {
        # protocol is http
        http_request++
        http_traffic += sc_bytes
    } else {
        https_request++
        https_traffic += sc_bytes
    }
    # parse log entry
    # cs_referer = $6
    # user_agent = $8
    yottaa_optimizations = $10
    yottaa_metrics = $12
    content_type = $14
    # x_forward_for = $16
    field17 = $17  # {s-domain} {cs-start-time} {cs-end-time} {sc-start-time} {sc-end-time}]
    # adn_id = $18
    get_cache_status(yottaa_optimizations)
    parse(sc_status, first_request_line, yottaa_optimizations, yottaa_metrics,    tmp)
    response_time = get_response_time(field17)
    if (content_type ~ /html/) {
        html_request++
        html_response_time += response_time
        first_byte += first_byte_time
    } else if (content_type ~ /javascript/) {
        javascript_request++
        javascript_response_time += response_time
    } else if (content_type ~ /css/) {
        css_request++
        css_response_time += response_time
    }
} END {
    sc_request = NR - cs_request
    if (sc_request == 0) {
        first_byte_avg = 0
    } else {
        first_byte_avg = first_byte / sc_request
    }
    if (html_request == 0) {
        html_response_time_avg = 0
    } else {
        html_response_time_avg = html_response_time / html_request
    }

    if (javascript_request == 0) {
        js_response_time_avg = 0
    } else {
        js_response_time_avg = js_response_time / javascript_request
    }

    if (css_request == 0) {
        css_response_time_avg = 0
    } else {
        css_response_time_avg = css_response_time / css_request
    }

    printf("cs_request=%d cs_traffic=%d cs_prefetch=%d http_request=%d http_traffic=%d https_request=%d https_traffic=%d hit=%d miss=%d status_2xx=%d status_3xx=%d status_4xx=%d status_5xx=%d yottaa_status_404=%d yottaa_status_5xx=%d os_timeout=%d html_response_time=%d js_response_time=%d css_response_time=%d first_byte=%d\n",
    cs_request,
    cs_traffic,
    cs_prefetch,
    http_request,
    http_traffic,
    https_request,
    https_traffic,
    hit,
    miss,
    status_2xx,
    status_3xx,
    status_4xx,
    status_5xx,
    yottaa_status_404,
    yottaa_status_5xx,
    os_timeout,
    html_response_time_avg,
    js_response_time_avg,
    css_response_time_avg,
    first_byte_avg)
}
