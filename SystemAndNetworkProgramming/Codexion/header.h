/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   header.h                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/12 17:34:10 by maziza            #+#    #+#             */
/*   Updated: 2026/06/30 18:54:57 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef HEADER_H
# define HEADER_H

# include <pthread.h>
# include "structs.h"
# include "colors.h"
# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <sys/time.h>
# include <unistd.h>

// Parsing
int				check_arg_int(char *arg);
int				filler(char **args, t_data *p_data);
void			fill_dongle(t_dongle *dongle, int cd);
t_coder			fill_coder(t_data *data, int id);

// Free values
int				free_all(pthread_t **threads, t_data *data);
int				free_values(int *values);
int				free_dongles(t_data *data);
int				free_coders(t_data *data);
int				free_states(t_data *data);

// Thread Management
void			*thread_function(void *arg);
int				is_dongle_ready(t_dongle dongle, t_coder *coder);
int				execute_function(int function(t_coder *, int, int),
					t_coder *coder, int left, int right);
int				compile(t_coder *coder, int left, int right);
int				debug(t_coder *coder, int left, int right);
int				refactor(t_coder *coder, int left, int right);
int				fifo(t_coder coder);
int				edf(t_coder coder);
void			swap(int *a, int *b, int cond);

// Queue

// Cooldowns
void			start_time(t_data *data);
void			update_time(t_coder *coder);
void			add_burnout(t_coder *coder);
long			get_time_up(t_coder *coder);
struct timespec	time_elapsed(struct timespec smaller, struct timespec bigger);

#endif
