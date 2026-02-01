/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   disorder.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jenicola <jean.nicolas-de-lamballerie@lea  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/26 15:37:28 by jenicola          #+#    #+#             */
/*   Updated: 2025/12/01 15:44:53 by jenicola         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

float	compute_disorder(int *a, unsigned int len)
{
	float			mistakes;
	float			total_pairs;
	unsigned int	i;
	unsigned int	j;

	mistakes = 0;
	total_pairs = 0;
	i = 0;
	j = 0;
	while (i < len)
	{
		j = i + 1;
		while (j < len)
		{
			total_pairs += 1;
			if (a[i] > a[j])
				mistakes += 1;
			j++;
		}
		i++;
	}
	if (mistakes == 0 || total_pairs == 0)
		return (0);
	return (mistakes / total_pairs);
}

int	displayable_disorder(float disorder)
{
	return ((int)(disorder * 10000));
}
