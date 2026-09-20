/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   queue.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/22 16:34:47 by maziza            #+#    #+#             */
/*   Updated: 2026/06/25 13:50:11 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"
#include <string.h>

void	update_queue_infos(t_coder *coder, int dongle_id)
{
	t_dongle	*dongle;

	dongle = &coder->data->dongles[dongle_id];
	if (coder->id == dongle_id)
	{
		dongle->right.id = coder->id;
		dongle->right.burnout = coder->spec;
		dongle->right.tv = coder->time;
	}
	else
	{
		dongle->left.id = coder->id;
		dongle->left.burnout = coder->spec;
		dongle->left.tv = coder->time;
	}
}

void	fifo(t_dongle *dongle)
{
	if (dongle->left.tv.tv_sec > dongle->right.tv.tv_sec)
		dongle->to_who = dongle->right.id;
	else if (dongle->left.tv.tv_sec < dongle->right.tv.tv_sec)
		dongle->to_who = dongle->left.id;
	else
	{
		if (dongle->left.tv.tv_usec > dongle->right.tv.tv_usec)
			dongle->to_who = dongle->right.id;
		else if (dongle->left.tv.tv_usec < dongle->right.tv.tv_usec)
			dongle->to_who = dongle->left.id;
		else
			dongle->to_who = -1;
	}
}

void	edf(t_dongle *dongle)
{
	if (dongle->left.burnout.tv_sec > dongle->right.burnout.tv_sec)
		dongle->to_who = dongle->right.id;
	else if (dongle->left.burnout.tv_sec < dongle->right.burnout.tv_sec)
		dongle->to_who = dongle->left.id;
	else
	{
		if (dongle->left.burnout.tv_nsec > dongle->right.burnout.tv_nsec)
			dongle->to_who = dongle->right.id;
		else if (dongle->left.burnout.tv_nsec < dongle->right.burnout.tv_nsec)
			dongle->to_who = dongle->left.id;
		else
			dongle->to_who = -1;
	}
}

int	next_coder(t_coder *coder, t_dongle *dongle)
{
	if (dongle->right.id == -1)
		dongle->to_who = (dongle->left.id + 1) % coder->params.nb_threads;
	else if (dongle->left.id == -1)
		dongle->to_who = (dongle->right.id - 1 + coder->params.nb_threads)
			% coder->params.nb_threads;
	else
	{
		if (!strcmp(coder->params.mode, "fifo"))
			fifo(dongle);
		// else if (!strcmp(coder->params.mode, "edf"))
		// 	edf(dongle);
		else
			dongle->to_who = -1;
	}
	return (0);
}

void	update_dongle_queue(t_coder *coder, int left, int right)
{
	update_queue_infos(coder, left);
	update_queue_infos(coder, right);
	next_coder(coder, &coder->data->dongles[left]);
	next_coder(coder, &coder->data->dongles[right]);
	return ;
}
