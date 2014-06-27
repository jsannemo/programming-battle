def solution_status(solution):
    if not solution:
        return '<td class="status"></td>'
    status = solution.status

    if status == 'defeated':
        bg = 'bg-danger'
    elif status == 'active':
        bg = 'bg-success'
    elif status == 'failed':
        bg = 'bg-warning'
    else:
        bg = 'bg-info'
    return '<td class="%s status"><a href="/solution/%d">%s</a></td>'%(bg, solution.solution_id, solution.get_status().display_name)


def testcase_status(solution):
    if not solution:
        return '<td class="status"></td>'
    status = solution.status

    if status == 'defeated':
        bg = 'bg-danger'
    elif status == 'active':
        bg = 'bg-success'
    elif status == 'rejected':
        bg = 'bg-warning'
    else:
        bg = 'bg-info'
    return '<td class="%s status"><a href="/solution/%d">%s</a></td>'%(bg, solution.testcase_id, solution.get_status().display_name)
