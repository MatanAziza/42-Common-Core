/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   structs.h                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/11 20:39:06 by maziza            #+#    #+#             */
/*   Updated: 2026/08/14 14:35:02 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef STRUCTS_H
# define STRUCTS_H

# include <bits/pthreadtypes.h>
# include <bits/types/struct_timeval.h>
# include <time.h>

enum					e_CoderState
{
	INIT,
	DONGLE,
	COMPILING,
	DEBUGGING,
	REFACTORING,
	FAILURE,
	SUCCESS
};

typedef struct s_params
{
	int					burnout_time;
	int					compile_time;
	int					debug_time;
	int					refactor_time;
	int					nb_compile;
	int					nb_threads;
	int					max_compile;
	int					dongle_cooldown;
	char				*mode;
}						t_params;

typedef struct s_node
{
	int					id;
	struct timeval		tv;
	struct timespec		burnout;
}						t_node;

typedef struct s_dongle
{
	int					to_who;
	int					cooldown;
	struct timespec		last_ts;
	struct timespec		ts;
	struct s_node		left;
	struct s_node		right;
	pthread_mutex_t		mutex_dongle;
	pthread_cond_t		cond_dongle;
}						t_dongle;

typedef struct s_log
{
	long				timestamp;
	int					id;
	enum e_CoderState	state;
}						t_log;

typedef struct s_status
{
	pthread_mutex_t		mutex_status;
	pthread_cond_t		cond_status;
	struct s_log		*status;
	int					length;
	int					counter;
	int					index;
}						t_status;

typedef struct s_data
{
	struct s_coder		*coders;
	struct s_dongle		*dongles;
	struct s_params		params;
	struct s_status		status;
	int					failure;
	int					start;
	struct timeval		time;
	struct timespec		spec;
}						t_data;

typedef struct s_coder
{
	int					id;
	struct timeval		time;
	struct timespec		spec;
	struct s_params		params;
	struct s_data		*data;
}						t_coder;
#endif
