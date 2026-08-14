/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/11 16:44:23 by maziza            #+#    #+#             */
/*   Updated: 2026/08/14 14:42:41 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"
#include "structs.h"
#include <bits/pthreadtypes.h>
#include <pthread.h>
#include <unistd.h>

void	create_threads(pthread_t **p_threads, t_data *data)
{
	pthread_t	*threads;
	int			i;

	threads = *p_threads;
	i = 0;
	data->start = 0;
	while (i < data->params.nb_threads)
	{
		pthread_create(&threads[i], NULL, thread_function, &data->coders[i]);
		i++;
	}
	usleep(1000000);
	start_time(data);
}

int	end_threads(pthread_t **p_threads, t_data *data)
{
	pthread_t	*threads;
	int			i;

	threads = *p_threads;
	i = 0;
	while (i < data->params.nb_threads)
		pthread_join(threads[i++], NULL);
	free_all(p_threads, data);
	return (1);
}

int	values_check(t_data *data)
{
	int	compile;
	int	refactor;
	int	debug;
	int	cooldown;

	compile = data->params.compile_time;
	refactor = data->params.refactor_time;
	debug = data->params.debug_time;
	cooldown = data->params.dongle_cooldown;
	if (data->params.burnout_time < compile + refactor + debug + cooldown)
		return (1 + 0 * printf("Cooldowns are superior to burnout.\n"));
	return (0);
}

void	init_status(t_data *data)
{
	int	i;
	int	messages;

	pthread_mutex_init(&data->status.mutex_status, NULL);
	pthread_cond_init(&data->status.cond_status, NULL);
	messages = (4 * data->params.max_compile + 1) * data->params.nb_threads;
	data->status.status = malloc(sizeof(struct s_log) * messages);
	i = 0;
	while (i < messages)
	{
		data->status.status[i].timestamp = 0;
		data->status.status[i].id = -1;
		data->status.status[i].state = INIT;
		i++;
	}
	data->status.length = messages;
	data->status.counter = 0;
	data->status.index = 0;
}

int	main(int argc, char **argv)
{
	t_data		data;
	pthread_t	*threads;

	if (argc != 9)
		return (0 * printf("Wrong number of args.\n"));
	if (filler(argv, &data))
		return (1);
	threads = malloc(sizeof(pthread_t) * (data.params.nb_threads + 1));
	if (!threads)
		return (1);
	if (values_check(&data))
		return (free_all(&threads, &data));
	init_status(&data);
	data.failure = 0;
	pthread_create(&threads[data.params.nb_threads], NULL, supervise, &data);
	create_threads(&threads, &data);
	pthread_join(threads[data.params.nb_threads], NULL);
	end_threads(&threads, &data);
	if (!data.failure)
		printf("%sSuccess: All threads compiled%s\n", GREEN, WHITE);
	return (0);
}
