/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strings.h                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jenicola <jean.nicolas-de-lamballerie@lea  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/28 13:35:17 by jenicola          #+#    #+#             */
/*   Updated: 2025/12/05 18:22:07 by jenicola         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_STRINGS_H
# define FT_STRINGS_H

# include "ft_errors.h"
# include <stddef.h>

size_t				ft_strlcpy(char *dst, const char *src, size_t size);
char				*ft_substr(char const *s, unsigned int start, size_t len);
size_t				ft_strlen(const char *s);
char				**ft_split(char const *s, char c);
int					ft_isdigit(int c);
void				increase_value(const char **ptr,
						t_conversion_result *result, int *idx);
t_conversion_result	ft_atol(const char *nptr);
#endif
