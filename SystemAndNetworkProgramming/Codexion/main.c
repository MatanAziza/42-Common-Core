/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/11 16:44:23 by maziza            #+#    #+#             */
/*   Updated: 2026/06/12 18:30:03 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"
#include "structs.h"
#include <pthread.h>
#include <unistd.h>

void	swap(int *a, int *b)
{
	int	swap;

	swap = *b;
	*b = *a;
	*a = swap;
}

void	*print_name(void *arg)
{
	t_coder	*coder;
	int		max;
	int		left;
	int		right;

	coder = (t_coder *)arg;
	max = coder->nb_threads;
	left = (coder->id + max - 1) % max;
	right = coder->id;
	if (right < left)
		swap(&right, &left);
	while (coder->nb_compile < coder->max_compile)
	{
		pthread_mutex_lock(&coder->dongles[left].mutex_dongle);
		pthread_mutex_lock(&coder->dongles[right].mutex_dongle);
		while (!coder->dongles[left].available)
			pthread_cond_wait(&coder->dongles[left].cond_dongle,
				&coder->dongles[left].mutex_dongle);
		coder->dongles[left].available = 0;
		while (!coder->dongles[right].available)
			pthread_cond_wait(&coder->dongles[right].cond_dongle,
				&coder->dongles[right].mutex_dongle);
		coder->dongles[right].available = 0;
		coder->nb_compile++;
		printf("Nb of compiles for Thread %d: %d\n", coder->id,
			coder->nb_compile);
		usleep(50000);
		coder->dongles[right].available = 1;
		coder->dongles[left].available = 1;
		pthread_cond_signal(&coder->dongles[left].cond_dongle);
		pthread_cond_signal(&coder->dongles[right].cond_dongle);
		pthread_mutex_unlock(&coder->dongles[left].mutex_dongle);
		pthread_mutex_unlock(&coder->dongles[right].mutex_dongle);
		usleep(50000);
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
	parser(argv, &data);
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
