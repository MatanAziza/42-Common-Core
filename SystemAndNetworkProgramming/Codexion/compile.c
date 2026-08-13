/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   compile.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/30 17:55:28 by maziza            #+#    #+#             */
/*   Updated: 2026/08/03 11:47:25 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"
#include "structs.h"
#include <errno.h>
#include <sys/time.h>

int	unlock(t_coder *coder, int left, int right)
{
	// To do: replace next 2 lines with queue to_who
	coder->data->dongles[left].to_who = -1;
	coder->data->dongles[right].to_who = -1;
	pthread_cond_signal(&coder->data->dongles[left].cond_dongle);
	pthread_cond_signal(&coder->data->dongles[right].cond_dongle);
	pthread_mutex_unlock(&coder->data->dongles[left].mutex_dongle);
	pthread_mutex_unlock(&coder->data->dongles[right].mutex_dongle);
	return (1);
}

int	wait(t_coder *coder, int left, int right)
{
	int	ret_l;
	int	ret_r;

	while (!is_dongle_ready(coder->data->dongles[left], coder)
		&& !is_dongle_ready(coder->data->dongles[right], coder))
	{
		ret_l = pthread_cond_timedwait(&coder->data->dongles[left].cond_dongle,
				&coder->data->dongles[left].mutex_dongle, &coder->spec);
		ret_r = pthread_cond_timedwait(&coder->data->dongles[right].cond_dongle,
				&coder->data->dongles[right].mutex_dongle, &coder->spec);
		if (ret_l == ETIMEDOUT || ret_r == ETIMEDOUT || coder->data->failure)
			return (1 + 0 *printf("FAIL\n"));
	}
	if (coder->data->failure)
		return (1 + 0 *printf("%d, FAIL\n", coder->id));
	update_time(coder, 0);
	change_status(get_time_up(coder), coder, DONGLE);
	return (0);
}

int	compile(t_coder *coder, int left, int right)
{
	add_burnout(coder);
	pthread_mutex_lock(&coder->data->dongles[left].mutex_dongle);
	pthread_mutex_lock(&coder->data->dongles[right].mutex_dongle);
	if (wait(coder, left, right)){
		update_time(coder, 0);
		// change_status(get_time_up(coder), coder, FAILURE);
		printf("haha\n");
		return (unlock(coder, left, right));
	}
	update_time(coder, 1);
	change_status(get_time_up(coder), coder, COMPILING);
	coder->data->dongles[left].to_who = coder->id;
	coder->data->dongles[right].to_who = coder->id;
	coder->params.nb_compile++;
	usleep(coder->params.compile_time * 1000);
	unlock(coder, left, right);
	return (0);
}
