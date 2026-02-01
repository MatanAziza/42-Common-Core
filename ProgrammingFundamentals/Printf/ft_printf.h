/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   libftprintf.h                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/10 14:14:31 by maziza            #+#    #+#             */
/*   Updated: 2025/11/10 14:18:04 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_PRINTF_H
# define FT_PRINTF_H

# include <stdarg.h>
# include <stdlib.h>
# include <unistd.h>

int	ft_putchar(char c);
int	ft_strlen(char *str);
int	ft_putstr(char *s);
int	ft_putnbr_base(long int nb, const char *base, int sign);
int	ft_print_address(unsigned long address, const char *base);
int	ft_check_flag(char c);
int	ft_printf(const char *flag, ...);
int	ft_putnbr_address(unsigned long nbr, const char *base);

#endif
