/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   structs.h                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/11 20:39:06 by maziza            #+#    #+#             */
/*   Updated: 2026/06/28 11:16:02 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef STRUCTS_H
# define STRUCTS_H

# include <bits/pthreadtypes.h>
# include <bits/types/struct_timeval.h>
# include <time.h>

enum					e_CoderState
{
	COMPILING,
	DEBUGGING,
	REFACTORING,
	INIT,
	WAITING,
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
	char				*mode;
}						t_params;

typedef struct s_node
{
	int					thread_id;
	struct timeval		time;
}						t_node;

typedef struct s_dongle
{
	int					to_who;
	int					cooldown;
	struct timespec		last_use;
	struct s_node		*queue;
	pthread_mutex_t		mutex_dongle;
	pthread_cond_t		cond_dongle;
}						t_dongle;

typedef struct s_data
{
	struct s_coder		*coders;
	struct s_dongle		*dongles;
	enum e_CoderState	*states;
	int					failure;
	struct s_params		params;
	int					start;
	struct timeval		time;
	struct timespec		spec;
}						t_data;

typedef struct s_coder
{
	int					id;
	struct timeval		time;
	struct timespec		spec;
	enum e_CoderState	state;
	struct s_params		params;
	struct s_data		*data;
}						t_coder;
#endif
