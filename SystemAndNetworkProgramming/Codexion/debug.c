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
	usleep(coder->params.debug_time * 1000);
	left += right;
	if (coder->data->failure)
		return (-2);
	gettimeofday(&coder->time, NULL);
	return (2);
}
