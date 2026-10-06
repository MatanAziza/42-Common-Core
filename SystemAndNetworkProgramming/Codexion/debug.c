/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   debug.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/30 17:56:19 by maziza            #+#    #+#             */
/*   Updated: 2026/06/30 18:53:49 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"
#include "structs.h"
#include <sys/time.h>

int	debug(t_coder *coder, int left, int right)
{
	change_status(coder, DEBUGGING);
	usleep(coder->params.debug_time * 1000);
	left += right;
	right -= left;
	if (coder->data->failure)
		return (1);
	return (0);
}
