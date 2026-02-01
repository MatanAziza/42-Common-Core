/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_atoi.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <maziza@student.42.fr>              +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/12 11:11:49 by maziza            #+#    #+#             */
/*   Updated: 2025/11/13 09:22:22 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
int	ft_atoi(const char *nptr)
{
	int	i;
	int	nbr;
	int	sign;

	nbr = 0;
	sign = 1;
	i = 0;
	while (nptr[i] == ' ' || nptr[i] == '\t' || nptr[i] == '\n'
		|| nptr[i] == '\v' || nptr[i] == '\f' || nptr[i] == '\r')
		i++;
	if (nptr[i] == '-')
	{
		sign = -1;
		i++;
	}
	else if (nptr[i] == '+')
		i++;
	while (nptr[i] >= '0' && nptr[i] <= '9')
	{
		nbr = 10 * nbr + nptr[i] - '0';
		i++;
	}
	return (sign * nbr);
}
