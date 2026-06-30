/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   refactor.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/30 17:56:47 by maziza            #+#    #+#             */
/*   Updated: 2026/06/30 18:02:01 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"
#include "structs.h"
#include <sys/time.h>

int	refactor(t_coder *coder, int left, int right)
{
	usleep(coder->params.refactor_time * 1000);
	left += right;
	if (coder->data->failure)
		return (-2);
	gettimeofday(&coder->time, NULL);
	return (3);
}
