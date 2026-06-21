/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   structs.h                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/11 20:39:06 by maziza            #+#    #+#             */
/*   Updated: 2026/06/12 18:30:01 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef STRUCTS_H
# define STRUCTS_H

# include <bits/pthreadtypes.h>

enum					e_CoderState
{
	COMPILING,
	DEBUGGING,
	REFACTORING,
	WAITING
};

typedef struct s_coder
{
	int					id;
	enum e_CoderState	state;
	int					burnout_time;
	int					compile_time;
	int					debug_time;
	int					refactor_time;
	int					nb_compile;
	int					nb_threads;
	int					max_compile;
	struct s_dongle		*dongles;
	struct s_queue		*queues;
}						t_coder;

typedef struct s_node
{
	int					thread_id;
	int					last_compile;
	int					burnout_time;
	struct s_node		*next;
}						t_node;

typedef struct s_queue
{
	struct s_node		*head;
}						t_queue;

typedef struct s_dongle
{
	int					available;
	int					to_who;
	int					cooldown;
	int					timer;
	pthread_mutex_t		mutex_dongle;
	pthread_cond_t		cond_dongle;
}						t_dongle;

typedef struct s_data
{
	struct s_coder		*coders;
	struct s_dongle		*dongles;
	struct s_queue		*queues;
}						t_data;

#endif
