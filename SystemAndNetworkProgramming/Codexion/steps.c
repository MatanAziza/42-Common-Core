/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   steps.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/28 11:23:58 by maziza            #+#    #+#             */
/*   Updated: 2026/06/30 19:11:34 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"
#include "structs.h"
#include <errno.h>
#include <sys/time.h>

int	execute_function(int function(t_coder *, int, int), t_coder *coder,
		int left, int right)
{
	int	result;

	result = function(coder, left, right);
	if (result == -2 || coder->data->failure)
		return (1);
	else if (result == -1)
	{
		coder->data->failure = 1;
		usleep(10000);
		return (1 + 0 * printf("%s%ld %d burned out\n", RED, get_time_up(coder),
				coder->id));
	}
	return (0);
}
