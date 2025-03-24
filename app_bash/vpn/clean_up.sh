# TODO: configure all back to default state


# Проверяем сетевое пространство. Если есть, то удаляем и создаем.
if ip netns list | grep -q "^$VPM_NAMESPACE"; then
  ip netns delete "$VPN_NAMESPACE"

  if [ $? -eq 0 ];then
    Logging "info" "Сетевое пространство $VPN_NAMESPACE уже существует."
    Logging "info" "Сетевое пространство $VPN_NAMESPACE успешно удаленно."
  else
    Logging "error"  "Ошибка при удалении сетевого пространства $VPN_NAMESPACE!"
    exit 1
  fi
fi

ip netns add "$VPN_NAMESPACE"

if [ $? -eq 0 ];then
  Logging "success" "Сетевое пространство $VPN_NAMESPACE успешно создано."
else
  Logging "error"  "Ошибка при создании сетевого пространства $VPN_NAMESPACE!"
  exit 1
fi

# Проверяем и если нет создаем интерфейс
if ip link show "$VETH_INTFS_DEFAULT_NS" > /dev/null 2>&1;then
  ip link delete "$VETH_INTFS_DEFAULT_NS"


  # Проверяем тип интерфейса
  intfs_type=$(ip link show "$VETH_INTFS_DEFAULT_NS" | grep -oP '(?<=link/)\w+')

  if [ "$infs_type" != "veth" ]; then
    Logging "error" "Ошибка! Интерфейс $VETH_INTFS_DEFAULT_NS уже существует, но его тип не соответствует. Текущий тип - $intfs_type."
    exit 1
  fi

  # Проверяем имя парного интерфейса
  peer_name=$(ip -d link show "$VETH_INTFS_DEFAULT_NS" | grep -oP "(?<=veth peer ifindex \d+ name )\w+)")

  if [ -z "$peer_name" ] || [ "$peer_name" != "$VETH_INTFS_VASE_NS" ]; then
    Logging "error" "Ошибка! Интерфейс $VETH_INTFS_DEFAULT_NS уже существует, но имя парного интерфейса не соответствует. Текущее имя - $peer_name."
    exit 1
  fi

  Logging "info" "Интерфейс $VETH_INTFS_DEFAULT_NS уже существует и соответствует конфигурации."

else
  ip link add "$VETH_INTFS_DEFAULT_NS" type veth peer name "$VETH_INTFS_VASE_NS."

    if [ $? -eq 0 ];then
      Logging "success" "Интерфейс $VETH_INTFS_DEFAULT_NS успешно создан."
    else
      Logging "error"  "Ошибка при создании интерфейса $VETH_INTFS_DEFAULT_NS!"
      exit 1
  fi
fi