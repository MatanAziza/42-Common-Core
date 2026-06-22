/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/11 16:44:23 by maziza            #+#    #+#             */
/*   Updated: 2026/06/22 17:30:37 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"
#include "structs.h"
#include <pthread.h>
#include <unistd.h>

void	swap(int *a, int *b, int cond)
{
	if (cond)
		return;
	int	swap;

	swap = *b;
	*b = *a;
	*a = swap;
}

int	GETTIMEOFDAY=10;

int	is_dongle_ready(t_dongle dongle, t_coder *coder)
{
	int	is_for_me;
	int	is_cd_done;

	is_cd_done = (GETTIMEOFDAY - dongle.last_use) >= dongle.cooldown;
	is_cd_done = 1;
	is_for_me = (dongle.to_who == coder->id || dongle.to_who == -1);
	return (is_cd_done && is_for_me);
}

void	gather_resources(t_coder *coder, int left, int right)
{
	pthread_mutex_lock(&coder->dongles[left].mutex_dongle);
	while (!is_dongle_ready(coder->dongles[left], coder))
	{
		printf("a");
		pthread_cond_wait(&coder->dongles[left].cond_dongle,
			&coder->dongles[left].mutex_dongle);
	}
	// coder->dongles[left].to_who = coder->id;
	pthread_mutex_lock(&coder->dongles[right].mutex_dongle);
	while (!is_dongle_ready(coder->dongles[right], coder))
		pthread_cond_wait(&coder->dongles[right].cond_dongle,
			&coder->dongles[right].mutex_dongle);
	// coder->dongles[right].to_who = coder->id;
	printf("%d, %d\n", coder->dongles[left].to_who, coder->dongles[right].to_who);
}

void	*print_name(void *arg)
{
	t_coder	*coder;
	int		left;
	int		right;

	coder = (t_coder *)arg;
	left = (coder->id + coder->nb_threads - 1) % coder->nb_threads;
	right = coder->id;
	swap(&right, &left, right < left);
	while (coder->nb_compile < coder->max_compile)
	{
		add_to_queues(coder);
		gather_resources(coder, left, right);
		coder->nb_compile++;
		printf("Nb of compiles for Thread %d: %d\n", coder->id,
			coder->nb_compile);
		usleep(500000);
		pthread_cond_signal(&coder->dongles[left].cond_dongle);
		pthread_cond_signal(&coder->dongles[right].cond_dongle);
		pthread_mutex_unlock(&coder->dongles[left].mutex_dongle);
		pthread_mutex_unlock(&coder->dongles[right].mutex_dongle);
		usleep(500000);
	}
	return (NULL);
}

int	main(int argc, char **argv)
{
	t_data		data;
	int			nb_threads;
	pthread_t	*threads;
	int			i;

	if (argc != 9)
		return (0 * printf("Wrong number of args.\n"));
	if (parse_check(argv))
		return (0 * printf("Wrong format of args.\n"));
	nb_threads = atoi(argv[1]);
	filler(argv, &data);
	i = 0;
	threads = malloc(sizeof(pthread_t) * nb_threads);
	while (i < nb_threads)
	{
		data.coders[i].nb_threads = nb_threads;
		pthread_create(&threads[i], NULL, print_name, &data.coders[i]);
		i++;
	}
	i = 0;
	while (i < nb_threads)
		pthread_join(threads[i++], NULL);
	free_data(data);
	free(threads);
	return (0);
}
