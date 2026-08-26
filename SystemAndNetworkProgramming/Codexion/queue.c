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
	// {
		dongle->to_who = dongle->right.id;
	// 	printf("right first\n");
	// }
	else if (dongle->left.tv.tv_sec < dongle->right.tv.tv_sec)
	// {
		dongle->to_who = dongle->left.id;
	// 	printf("left first\n");
	// }
	else
	{
		if (dongle->left.tv.tv_usec > dongle->right.tv.tv_usec)
		// {
			dongle->to_who = dongle->right.id;
		// 	printf("miniright first\n");
		// }
		else if (dongle->left.tv.tv_usec < dongle->right.tv.tv_usec)
		// {
			dongle->to_who = dongle->left.id;
			// printf("minileft first\n");
		// }
		else
		// {
			dongle->to_who = dongle->left.id;
			// printf("last option\n");
		// }
	}
}

void	edf(t_dongle *dongle)
{
	dongle->to_who = -1;
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
	printf("\033[1;37mDongle for %d and %d to_who: %d\n", dongle->left.id,
		dongle->right.id, dongle->to_who);
	return (0);
}

void	update_dongle_queue(t_coder *coder, int left, int right)
{
	// Changer ses infos dans les 2 dongles
	update_queue_infos(coder, left);
	update_queue_infos(coder, right);
	// appeler fonction 2 fois qui renvoie a chaque dongle
	// l'id du to_who (selon fifo ou edf)
	next_coder(coder, &coder->data->dongles[left]);
	next_coder(coder, &coder->data->dongles[right]);
	return ;
}
